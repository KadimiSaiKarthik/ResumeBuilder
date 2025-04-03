# ResumeBuilder
 It is a python commandline script that generates a pdf based on API data

# Feature 
coming to features it has the following features:
->fetches details from an API
->Customizable font size and colours
->generates the output in pdf 

# Installation
1)python
2)install packages
  ->fpdf
  ->requests
  ->argsparse

# how to use
# example:(run this command)
python ResumeBuilder.py --name "Sai Karthik" --font-size 15 --font-color "#333333" --background-color "#F5F5F5" --output "KarthikResume.pdf"--verbose
# Arguments to be used 
--name	(Name of the person)	
--font-size	(Font size for the resume)	
--font-color	(Hex color code for text color)
--background-color	(Hex color code for background)
--output	(Name of the output PDF file)

# this how it would look
![image](https://github.com/user-attachments/assets/820e587d-c4ac-4827-9a01-807dea154c60)


# API used
https://expressjs-api-resume-random.onrender.com/resume?name=YOUR_NAME

# the Requirements of the version are mentioned in the requirements.txt

