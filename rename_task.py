import os
import re
import sys
from datetime import datetime
from pypdf import PdfReader

# =========================================================================
# 🛑 সুরক্ষার জন্য মেয়াদের শেষ তারিখ (বছর, মাস, দিন)
# এই তারিখ পার হয়ে গেলে সফটওয়্যার আর কাজ করবে না। 
# আপনি নিজের জন্য তারিখটি বাড়িয়ে ২০২৭, ২০৩০ বা যা খুশি করে নিতে পারবেন।
# =========================================================================
EXPIRY_DATE = datetime(2026, 12, 31) 

def normalize_text(text):
    if not text: return ""
    # Keeps only lowercase alphanumeric characters for better matching
    return re.sub(r'[^a-z0-9]', '', str(text).lower())

def start_renaming(path, names_list, extra_info=""):
    path = path.strip('"').strip("'").strip()
    if os.path.isfile(path): path = os.path.dirname(path)
    if not os.path.exists(path):
        print(f"Error: The specified folder path was not found!")
        return

    print(f"\nProcessing files... Please wait.\n")
    files = [f for f in os.listdir(path) if f.lower().endswith('.pdf')]
    if not files:
        print("No PDF files found in the directory.")
        return

    # Sort names by length (descending) to avoid partial matches
    sorted_names = sorted(names_list, key=len, reverse=True)
    normalized_targets = [(normalize_text(n), n) for n in sorted_names]

    success_count = 0
    fail_count = 0

    for filename in files:
        file_full_path = os.path.join(path, filename)
        try:
            reader = PdfReader(file_full_path)
            # Extracts text from the first page
            content = reader.pages[0].extract_text()
            if not content:
                print(f"Skipped: Could not read text from {filename}")
                fail_count += 1
                continue
            
            clean_content = normalize_text(content)
            found_original_name = None
            
            # Check for a match in the customer list
            for clean_target, original_name in normalized_targets:
                if clean_target in clean_content:
                    found_original_name = original_name
                    break
            
            if found_original_name:
                # Remove invalid characters for Windows filenames
                clean_filename_part = re.sub(r'[\\/*?:"<>|]', "", found_original_name)
                
                # Append extra info if provided
                if extra_info.strip():
                    new_filename = f"{clean_filename_part} {extra_info.strip()}.pdf"
                else:
                    new_filename = f"{clean_filename_part}.pdf"
                
                new_full_path = os.path.join(path, new_filename)
                
                # Handle duplicate filenames in the same folder
                count = 1
                base_name_only = os.path.splitext(new_filename)[0]
                while os.path.exists(new_full_path):
                    new_full_path = os.path.join(path, f"{base_name_only}_{count}.pdf")
                    count += 1
                
                os.rename(file_full_path, new_full_path)
                print(f"Success: {filename} -> {os.path.basename(new_full_path)}")
                success_count += 1
            else:
                print(f"Not Matched: No name from list found inside {filename}")
                fail_count += 1

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            fail_count += 1

    print("\n" + "-"*30)
    print(f"TASK COMPLETED")
    print(f"Successfully Renamed: {success_count}")
    print(f"Failed or Not Matched: {fail_count}")
    print("-"*30)

if __name__ == "__main__":
    # 🔒 সফটওয়্যার রান হওয়ার সাথে সাথেই বর্তমান তারিখ চেক করা হচ্ছে
    if datetime.now() > EXPIRY_DATE:
        print("\n" + "!"*60)
        print("Error: This software version has expired!")
        print("Please contact the original developer for an updated version.")
        print("!"*60)
        input("\nPress Enter to exit...")
        sys.exit()

    # Your full customer list
    target_names = [
        "Abdul Hardware", "Abhijit Pal", "Acharjee Hardware", "Adhikary Iron", "Anirban Builders", 
        "Annapurna Hardware", "Annapurna Supliers", "Antara Das", "Ashok Halder Iron Stores", 
        "B. M. B. Builders", "B. R. Traders", "Balailal Hardware", "Bhai Bhai Builders", 
        "Bhattacharya Hardware", "Biswakarma Builders", "Biswas Builders And Hardware", 
        "Biswas Hardware", "Chandan Kumar Patwa", "Debnath Brothers", "Deep Steel", 
        "Dutta Builders", "Dutta Builders And Hardware", "Ghosh Builders-Haringhata", 
        "Ghosh Builders-Ramnagar", "Gopal Builders", "Jana Builders", 
        "K. S. Stone Chips and Sand Co", "Kalimata Builders", "Kanai Chandra Dey", 
        "Karunamayee Hardware", "Kundu Brothers", "Loknath Hardwares & Builders", 
        "Maa Shitala Hardware", "Maa Tara Builders", "Maa Tara Traders", 
        "Maa Traders And Builders", "Mahaprabhu H/W Stores", "Majumder Builders", 
        "Malakar Enterprise", "Mallick Hardware", "Mamtaj Builders", "Mandal Builders", 
        "Manju Hardware", "Maya Steel & Paint", "Monarama Builders & Enterprise", 
        "Mondal Hardware And Builders", "Nepal Chandra Ghosh & Sons", "New Gopal Bhandar", 
        "New Krishnagar Hardware", "New Maa Manasa Builders", "New Pal Builders", 
        "New Radhakrishna Enterprise", "New Sadhana Builders", "Nibash Saha", 
        "NKP Hardwares", "Paltu Builders And Suppliers", "Paul Hardware And Builders", 
        "Paul Traders - Nadia", "Priya Traders", "Putul Builders & Suppliers", 
        "Radhakrishna Builders", "Ramkrishna Hardware", "Roy Enterprises", "Rudra Traders", 
        "S. S. Enterprise", "Sabitri Hardware", "Saha Build Co", "Sanika Builders", 
        "Sarkar Hardware", "Satabdi Builders", "Shibom Enterprise", "Soma Sarkar", 
        "Sri Krishna Suppliers", "Sridharnath Traders", "Srikrishna Builders", 
        "Sudha Builders & Padarpan", "Sulekha Traders", "Tinku Hardware", "Uma Builders", 
        "Usha Traders", "Vivekananda Panja", "Mani Sankar Sadhukhan", "B S Enterprise", 
        "K Steel Shibom Tarama Hardwares", "ABHAY HARDWARE STORES", "A.D.TRADERS", 
        "AHAD BUILDERS", "AMBIKA PAL", "ANNAPURNA TRADERS", "APU ENTERPRISE", 
        "APURBA ENTERPRISE", "APPAYAN HARDWARE & TILES", "ASHOK HARDWARE & VARIETY STORES", 
        "BHOWMICK ENTERPRISE", "BABU HARDWARE", "BABLU HARDWARE", "BABA KARAMPIR HARDWARE", 
        "BANERJEE HARDWARE", "BIKASH SAMUI", "BULBULITALA ENTERPRISE", "CHATTERJEE SUPPLIERS", 
        "CHIP HARDWARE STORE", "CIVIL CONTRACTOR & GENERAL ORDER", "C M BUILDERS & HARDWARE", 
        "DAS IRON & STEEL", "DAWN BUILDERS", "DEY HARDWARE AND PAINTS", "DURGA MATA TRADING COMPANY", 
        "FRIENDS STEEL", "GHOSH ENTERPRISE-SHIMULIA CHATI", "GHOSH ENTERPRISE", "GHOSH HARDWARE", 
        "GOPAL TRADERS", "HALDER CONDEV PVT. LTD.", "HAZRA LOUHA BIPONI", "INAAYA ENTERPRISE", 
        "JAGANANDA SUPPLIERS", "JANANI BUILDERS", "JAYABRATA PAL", "JOYGURU HARDWARE", 
        "JYOTI BUILDERS", "KALIMATA TRADERS", "KAMINI MATA BUILDERS", "KAMINI MATA TRADERS", 
        "KANAKLATA HARDWARE", "KARMAKAR HARDWARE-GOLAPBAG", "KARMAKAR HARDWARE-COLLEGE MORE", 
        "KARTICK CHANDRA DAS", "KEYA BUILDERS", "KHAJA BABA HARDWARE", "KOHINOOR HARDWARE", 
        "MA TARA PAINTS AND HARDWARE", "MA TARA TRADERS", "MAA CHAMUNDA HARDWARE", 
        "MAA HARDWARE STORES", "MAA KALI BUILDERS", "MAA KALI HARDWARE", 
        "MAA JAGADHATRI ENTERPRISE", "MAA LAKSHMI TRADES", "MAA MANOSA TRADERS", 
        "MAA RAKSHAKALI ENTERPRISE", "MAA SAGARIKA ENTERPRISE", "MADHUSUDAN DEY", 
        "MANIK TRADERS", "MASTER BUILDERS", "MEGNA ENTERPRISE", "MIRJA COLOUR HOUSE", 
        "MIRJA SUPPLIERS", "MITHU AND SONS HARDWARE", "MITRA BUILDERS", "MRINMAYEE CITY STEEL", 
        "M.H.HARDWARE", "M.K PAL", "MONDAL HARDWARE", "MONDAL TRADERS", "MUKHERJEE TYLES HOUSE", 
        "NAG ASSOCIATES", "NARAYAN BUILDERS", "NATIONAL HARDWARE STORES", "NEW AHAMMAD CEMENT CENTER", 
        "NEW ALAMEEN HARDWARE", "NEW JOY BABA LOKENATH HARDWARE", "NEW ROY HARDAWRE", 
        "NEW SAHA BUILDERS", "NEW SAHA TRADERS", "NEW M.D.ENTERPRISE", "NAYAK HARDWARE", 
        "PAPAI HARDWARE", "PAL ENTERPRISE", "PANCHANAN HARDWARE STORES", "PINTU GHOSH", 
        "RADHARANI STEEL & IRON", "RADHA KANTA SOM", "RADHA MADHAB TRADERS", "RAJ ENTERPRISE", 
        "RAJIB MONDAL", "RAMKRISHNA ENTERPRISE", "RANGA SHREE HARDWARE", 
        "RIMI CONSTRUCTION AND GENERAL ORDER SUPPLIER", "ROY ENTERPRISE-CHAKDIGHI", 
        "ROY ENTERPRISE-BHATAR", "SADHANA BUILDERS & HARDWARE", "SAHEB JAN SEKH", 
        "SAKIL HARDWARES", "SAMANTA HARDWARE", "SAMANTA ENTERPRISE", "SAMRAT ENTERPRISE", 
        "SANJIB DAS", "SATGACHIA HARDWARE STORES", "SATHI ENTERPRISE", "SATTWIK TRADERS", 
        "SEKH.G.BUILDERS & HARDWARE", "SHREE KRISHNA TRADERS", "S R HARDWARE", 
        "S.K. HARDWARE", "SIFA CONSTRUCTION", "SINGHA RAY CONSTRUCTION", "SK. ASRAF ALI", 
        "S K BROTHERS", "SK. NIAMUL HAQUE", "SOUVIK BANERJEE", "SREE DURGA HARDWARE AND TRADERS", 
        "SREE DURGA TRADERS", "SREE NARAYAN BUILDERS", "STHAPATI", "SUCHANA", "SUHANA ENTERPRISE", 
        "SURYA TRADERS", "SUSOVAN SAHA", "TARA MAA BUILDERS", "THE M/S BAIDYA NATH RAY", 
        "TORSHA HARDWARE", "TRINAYANI HARDWARE", "UTTAM KUMAR PAL", "UTPAL GHOSH", 
        "VIVEKANANDA ENTERPRISE", "WORLD BUILDERS"
    ]

    while True:
        print("\n" + "="*60)
        pdf_folder = input("1. Enter PDF Folder Path (or press Enter to Exit): ")
        if not pdf_folder.strip():
            print("Exiting application. Goodbye!")
            break
            
        extra = input("2. Enter suffix to add to name (e.g., March-2026) or press Enter to skip: ")
        
        start_renaming(pdf_folder, target_names, extra)
