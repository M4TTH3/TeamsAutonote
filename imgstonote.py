from PIL import Image
import io
from easyocr import Reader
from pathlib import Path
from fpdf import FPDF

class ImgToNote:

    def __init__(self, imgs: list[bytes] = None) -> None:
        if imgs == None:
            imgs = []

        self.text = ""
        self.image_gallery: list[bytes] = []
        self.ocr = Reader(['en'])
        self.bytelen = 0

        for i in imgs:
            self.update_text(i)

            if self.bytelen == 0:
                self.bytelen = len(i)


    def get_gallery(self) -> list[Image.Image]:
        ret = []
        for i in self.image_gallery:
            ret.append(Image.open(io.BytesIO(i)))
        
        return ret


    def insert_image(self, img: bytes) -> None:
        "Inserts the image into the 'note' if it's a new image from previous"
        if self.bytelen == 0:
                self.bytelen = len(img)

        # Compare to the last inserted image
        if len(self.image_gallery) > 0:
            if self.compare_image(img, self.image_gallery[-1], self.bytelen):
                return None
        
        self.update_text(img)


    def update_text(self, img: bytes) -> None:
        "Adds an to gallery and updates text"
        read = "".join(self.ocr.readtext(img, detail=0))
        self.text = self.text + read + "\n"
        self.image_gallery.append(img)

    
    def generate_slide(self, path: Path | str) -> None:
        """Generates a pdf of all the images to the desired path"""
        pdf = FPDF(orientation="P", unit="pt", format="A4")
        pdf.add_page()

        for img in self.image_gallery:
            with io.BytesIO(img) as data:
                pdf.image(data, w=500, h=400, x=int(pdf.w / 2 - 250))

                # Make a gap between each image
                pdf.set_font("Times", size=24)
                pdf.cell(w=pdf.w, h=30, new_x='LMARGIN', new_y='NEXT') 
        
        pdf.output(path)


    def make_note(self) -> None:
        pass

    
    @staticmethod
    def summarize(text):
        import openai
        import os
        openai.api_key = os.getenv('gptkey')

        chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You summarize text and fill in details to generate a study note"},
                {"role": "user", "content": f"Convert the following text into a study note: {text}"},
            ]
        )

        return str(chat['choices'][0]['message']['content'])


    @staticmethod
    def compare_image(img1: bytes, img2: bytes, length: int, factor=0.75) -> bool:
        """Compares the similarity of two images if it's within a factor 0 -> 1 assuming equal sizes.
        Use a sample of 1/10 of the pixels from the middle of the image"""
        equal = 0

        samplesize = int(length / 20) # x2 for both sides of half
        half = int(length / 2)
        for i in range(half - samplesize, half + samplesize):
            if img1[i] == img2[i]:
                equal += 1

        if equal / (samplesize * 2) >= factor:
            return True 

        return False

im1 = Image.open('s1.png')
im2 = Image.open('s2.png')
im2c = Image.open('copy-s2.png')
im3 = Image.open('s3.png')
im4 = Image.open('s4.png')

l = [im1, im2, im2c, im3, im4]

itn = ImgToNote()

for item in l:
    b = io.BytesIO()
    item.save(b, 'png')
    itn.insert_image(b.getvalue())

# ImgToNote.compare_image()

itn.generate_slide('output.pdf')
print(itn.text)

# print(ImgToNote.compare_image(data, data, len(data), 1))
# itn.insert_image(None)