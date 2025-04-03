import argparse 
import requests 
from fpdf import FPDF
from datetime import datetime

# getting the data from api via the name
def resume_data(name):
    url=f"https://expressjs-api-resume-random.onrender.com/resume?name={name}"
    try:
        response=requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"error fetching resume data:{e}")
        return None

#changing the hex code to rbg code  
def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

# converting the format of date to month followed by year
def format_date(date_str):
    if not date_str or date_str.lower()=="present":
        return "Present"
    try:
        return datetime.strptime(date_str,"%Y-%m-%d").strftime("%b %Y")
    except ValueError:
        return date_str

#the main pdf generation 
def generated_pdf(name,font_size,font_color,background_color,output_pdf):
    data= resume_data(name)
    if not  data:
        return
    pdf=FPDF()
    pdf.set_auto_page_break(auto=True,margin=15)
    pdf.set_left_margin(5)
    pdf.add_page()

    #setting up the background colour
    r,g,b=hex_to_rgb(background_color)
    pdf.set_fill_color(r,g,b)
    pdf.rect(0,0,210,297,style='F')

    # setting the font colour      
    r,g,b=hex_to_rgb(font_color)
    pdf.set_text_color(r,g,b)

    #setting the font style
    pdf.set_font("Helvetica",style="B",size=font_size+6)
    line_height=max(7,font_size*0.7)

    #Adding the name
    pdf.cell(200,10,data.get("name","Name not found"),ln=True,align="L")
    pdf.ln(5)

    #personal details
    pdf.set_font("helvetica",size=font_size)
    for key in ["email","phone","address"]:
        value=data.get(key,"N/A")
        if value!="N/A":    
            pdf.cell(200,line_height,value,ln=True,align="L")
    pdf.line(10, pdf.get_y(), 200,pdf.get_y())
    pdf.ln(5)

    #first break (the summary section)
    summary=data.get("summary","").strip()
    if summary:
        pdf.set_font("Helvetica",style="B",size=font_size+4)
        pdf.multi_cell(0,line_height,"Personal & Proffessional Overview")
        pdf.set_font("Helvetica",size=font_size)
        pdf.multi_cell(0,line_height,summary)
        pdf.line(10,pdf.get_y(),200,pdf.get_y())
        pdf.ln(5)  

    # the skills section 
    pdf.set_font("Helvetica",style="B",size=font_size+4)
    pdf.multi_cell(0,line_height,"Core Skills & Competencies")
    pdf.set_font("Helvetica",size=font_size)
    skills=data.get("skills",[])
    column_width=95
    for i in range(0, len(skills), 2):
        skill1 = skills[i]
        skill2 = skills[i+1] if i+1 < len(skills) else ""
        pdf.cell(column_width, line_height, skill1, border=0, ln=False)
        pdf.cell(column_width, line_height, skill2, border=0, ln=True)
    pdf.line(10,pdf.get_y(),200,pdf.get_y())
    pdf.ln(5)  

    #experiences and projects section
    pdf.set_font("Helvetica",style="B",size=font_size+4)
    pdf.multi_cell(0,line_height,"Work Experience & Key Projects")
    pdf.ln(2)
    
    for project in data.get("projects",[]):
        pdf.set_font("Helvetica","B",font_size)

        #Title
        title=project.get("title","Untitled Project")
        #Date
        start_date=format_date(project.get("startDate",""))
        end_date=format_date(project.get("endDate","Present"))
        date_range=f"{start_date}-{end_date}"

        pdf.cell(150,line_height,f"{title}",ln=False)
        pdf.cell(50,line_height,date_range,ln=True,align="R")

        pdf.set_font("Helvetica",size=font_size)
        pdf.multi_cell(0,line_height,project.get("description",""))
        pdf.ln(5)

    pdf.output(output_pdf)
    print(f"resume is succesfully generated:{output_pdf}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Customizable Resume Builder")
    parser.add_argument("--name", required=True, help="Full Name for resume")
    parser.add_argument("--font-size", type=int, default=12, help="Font size for the resume")
    parser.add_argument("--font-color", default="#", help="Font colour(hex code)")
    parser.add_argument("--background-color", default="#000000", help="Background colour(hex code)")
    parser.add_argument("--output", default="resume.pdf", help="Output PDF file name")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    
    if args.verbose:
        print(f"Generating resume for {args.name} with font size {args.font_size}, font color {args.font_color}, background color {args.background_color}, output file {args.output}")

    generated_pdf(args.name, args.font_size, args.font_color, args.background_color, args.output)

    



