import os
import fitz  # PyMuPDF
from PIL import Image, ImageDraw

def generate_sample_pdf(output_path):
    # 1. Create a dummy image to embed in the PDF
    image_path = "temp_embedded_logo.png"
    img = Image.new('RGB', (200, 100), color='#1e3a8a')
    d = ImageDraw.Draw(img)
    d.text((10, 40), "PATRANET LOGO", fill=(255, 255, 255))
    img.save(image_path)
    
    # 2. Create a new PDF document using PyMuPDF
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4 size in points
    
    # 3. Add the image logo
    rect = fitz.Rect(50, 50, 150, 100)
    page.insert_image(rect, filename=image_path)
    
    # 4. Insert some heading and billing text (using default standard font)
    page.insert_text((180, 70), "INVOICE: #INV-2026-9912", fontsize=16)
    page.insert_text((180, 90), "Date: May 30, 2026", fontsize=10)
    page.insert_text((180, 105), "Due Date: June 15, 2026", fontsize=10)
    
    # Billing Info
    page.insert_text((50, 170), "Billed To:", fontsize=12)
    page.insert_text((50, 185), "Hackathon Jury Evaluator", fontsize=10)
    page.insert_text((50, 198), "Google Hackathon HQ, Stage 1", fontsize=10)
    
    page.insert_text((350, 170), "Sender:", fontsize=12)
    page.insert_text((350, 185), "PATRANET IDP LLC", fontsize=10)
    page.insert_text((350, 198), "Innovations Space, Core A", fontsize=10)
    
    # 5. Insert structured text representing a table
    # Draw table border lines
    shape = page.new_shape()
    # Headers outline
    shape.draw_rect(fitz.Rect(50, 250, 545, 275))
    # Rows outline
    shape.draw_rect(fitz.Rect(50, 250, 545, 375))
    
    # Column dividers
    shape.draw_line(fitz.Point(300, 250), fitz.Point(300, 375))
    shape.draw_line(fitz.Point(380, 250), fitz.Point(380, 375))
    shape.draw_line(fitz.Point(460, 250), fitz.Point(460, 375))
    
    # Row dividers
    shape.draw_line(fitz.Point(50, 275), fitz.Point(545, 275))
    shape.draw_line(fitz.Point(50, 300), fitz.Point(545, 300))
    shape.draw_line(fitz.Point(50, 325), fitz.Point(545, 325))
    shape.draw_line(fitz.Point(50, 350), fitz.Point(545, 350))
    
    # Commit table drawings
    shape.commit()
    
    # Insert Table Header Text
    page.insert_text((60, 267), "Item Description", fontsize=10)
    page.insert_text((310, 267), "Quantity", fontsize=10)
    page.insert_text((390, 267), "Unit Price", fontsize=10)
    page.insert_text((470, 267), "Total Price", fontsize=10)
    
    # Row 1
    page.insert_text((60, 292), "Cloud Server hosting - Pro Plan", fontsize=9)
    page.insert_text((310, 292), "2", fontsize=9)
    page.insert_text((390, 292), "$150.00", fontsize=9)
    page.insert_text((470, 292), "$300.00", fontsize=9)
    
    # Row 2
    page.insert_text((60, 317), "Database Storage Upgrade (1TB)", fontsize=9)
    page.insert_text((310, 317), "1", fontsize=9)
    page.insert_text((390, 317), "$250.00", fontsize=9)
    page.insert_text((470, 317), "$250.00", fontsize=9)
    
    # Row 3
    page.insert_text((60, 342), "Premium SSL Certificates", fontsize=9)
    page.insert_text((310, 342), "5", fontsize=9)
    page.insert_text((390, 342), "$40.00", fontsize=9)
    page.insert_text((470, 342), "$200.00", fontsize=9)
    
    # Row 4
    page.insert_text((60, 367), "Support SLA - Enterprise Tier", fontsize=9)
    page.insert_text((310, 367), "1", fontsize=9)
    page.insert_text((390, 367), "$700.00", fontsize=9)
    page.insert_text((470, 367), "$700.00", fontsize=9)
    
    # Total calculation block
    page.insert_text((380, 410), "Grand Total:", fontsize=12)
    page.insert_text((470, 410), "$1,450.00", fontsize=12)
    
    # Footnote
    page.insert_text((50, 750), "Notes: Thank you for your business. Let's make PATRANET win the hackathon!", fontsize=10)
    
    # Save the output PDF
    doc.save(output_path)
    doc.close()
    
    # Clean up temp logo image
    if os.path.exists(image_path):
        os.remove(image_path)
        
    print(f"Sample PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    generate_sample_pdf("PATRANET_Sample_Document.pdf")
