#Ian Setia, Andrew Linares
#isetia@nd.edu, alinare2@nd.edu

import argparse, os, docx, sys

# Converts text file to text string
def read_text_file(text_file):
    with open(text_file, 'r') as file:
        return file.read()

def create_stat_table(doc, stats):
    # Creates a table in the docx and fills the top row with headers
    table = doc.add_table(rows=1, cols=2)
    header = table.rows[0].cells
    header[0].text = "Statistic"
    header[1].text = "Value"

    # Fills the rest of table with data
    for key, value in stats.items():
        row = table.add_row().cells
        row[0].text = key
        row[1].text = str(value)
    
def generate_report(text, stats, png, output):
    doc = docx.Document()
    doc.add_heading("Report")
    doc.add_paragraph(text)
    create_stat_table(doc, stats)
    doc.add_picture(png)
    doc.save(output)
    print("{} was successfully generated".format(output))

def main():
    parser = argparse.ArgumentParser(description="Generate a Word Document from text file and png file")
    parser.add_argument("text_file", type=str, help="Path to text file")
    parser.add_argument("png_file", type=str, help="Path to png image")
    parser.add_argument("output_file", type=str, help="Path to output Word Document")
    args = parser.parse_args()

    if not os.path.isfile(args.text_file):
        print("Error: The text file {} does not exist".format(args.text_file))
        return
    if not os.path.isfile(args.png_file):
        print("Error: The png file {} does not exist".format(args.png_file))
        return   

    text = read_text_file(args.text_file)
    
    stats = {
        "Period" : "All",
        "Interface" : "Wired",
        "Num Points" : 2,
        "Min" : 0,
        "Max" : 0,
        "Mean" : 0,
        "Median" : 0,
        "Std Dev" : 0,
        "10th Percentile" : 0,
        "90th Percentile" : 0
    }
        
    generate_report(text, stats, args.png_file, args.output_file)
 

if __name__ == "__main__":
    main()
