from wand.image import Image as Img
from PIL import Image
import pytesseract


def collect_data():
    """Gets data from given pdf, returns dict"""
    with Img(filename='PRISM.pdf', resolution=300) as img:
        # img.compression_quality = 99
        img.save(filename='test.png')

        img = Image.open('test-0.png')

        # Document Title
        doc_title = img.crop((80, 125, 2030, 420))
        doc_title.save('title.png')

        # Choose One: Cooperative Agreement or Grant
        cooperative_agreement = img.crop((2096, 208, 2128, 240))
        cooperative_agreement.save('cooperative_agreement.png')
        grant = img.crop((2098, 306, 2130, 336))
        grant.save('grant.png')

        # Choose One: Education, Facilities, Research, SDCR, Training
        education = img.crop((461, 444, 491, 470))
        education.save('education.png')
        facilities = img.crop((895, 444, 926, 470))
        facilities.save('facilities.png')
        research = img.crop((1280, 444, 1310, 470))
        research.save('research.png')
        sdcr = img.crop((1736, 444, 1764, 470))
        sdcr.save('sdcr.png')
        training = img.crop((2094, 444, 2122, 470))
        training.save('training.png')

        # 1. Grant/Cooperative Agreement Number
        agreement_number = img.crop((85, 592, 984, 634))
        agreement_number.save('agreement_number.png')

        # 2. Supplement Number
        supplement_number = img.crop((1006, 592, 1566, 634))
        supplement_number.save('supplement_number.png')

        # 3. Effective Date
        effective_date = img.crop((1579, 592, 2028, 634))
        effective_date.save('effective_date.png')

        # 4. Completion Date
        completion_date = img.crop((2049, 592, 2443, 634))
        completion_date.save('completion_date.png')

        # 5. Issued To - Name/Address of Recipient(No., Street, City/County, State, Zip)
        # 6. Issued By - Mailing Address

        # 7. Taxpayer Identification No. (TIN)
        taxpayer_id = img.crop((85, 1040, 1145, 1075))
        taxpayer_id.save('taxpayer_id.png')

        # 8. Commercial & Government Entity (CAGE) No.
        cage_num = img.crop((80, 1140, 1145, 1175))
        cage_num.save('cage_num.png')

        # 9. Principal Investigator/Organization's Project or Program MGR. (Name & Phone)
        pi_name_phone = img.crop((1165, 1060, 2460, 1110))
        pi_name_phone.save('pi_name_phone.png')
        pi_email = img.crop((1165, 1115, 2460, 1170))
        pi_email.save('pi_email.png')

        # 10. Research, Project, or Program Title
        project_title = img.crop((79, 1223, 2460, 1325))
        project_title.save('project_title.png')

        # 11. Purpose
        purpose = img.crop((79, 1378, 2460, 1480))
        purpose.save('purpose.png')

        # 12. Period of Performance (Approximately)
        period_of_performance = img.crop((79, 1532, 2460, 1580))
        period_of_performance.save('period_of_performance.png')

        # 13A. Award History - Previous, This Action, Cash Share, Non-Cash Share, Recipient Share, Total
        aw_previous = img.crop((516, 1640, 1240, 1679))
        aw_previous.save('aw_previous.png')
        aw_action = img.crop((516, 1688, 1240, 1727))
        aw_action.save('aw_action.png')
        aw_cash_share = img.crop((516, 1735, 1240, 1779))
        aw_cash_share.save('aw_cash_share.png')
        aw_non_cash_share = img.crop((516, 1786, 1240, 1829))
        aw_non_cash_share.save('aw_non_cash_share.png')
        aw_recipient_share = img.crop((516, 1837, 1240, 1879))
        aw_recipient_share.save('aw_recipient_share.png')
        aw_total = img.crop((516, 1888, 1240, 1929))
        aw_total.save('aw_total.png')

        # 13B. Funding History - Previous, This Action, Total
        fh_previous = img.crop((1720, 1640, 2465, 1679))
        fh_previous.save('fh_previous.png')
        fh_action = img.crop((1720, 1688, 2465, 1727))
        fh_action.save('fh_action.png')
        fh_total = img.crop((1720, 1735, 2465, 1780))
        fh_total.save('fh_total.png')

        # 14. Accounting and Appropriation Data

        # 15. Points of Contact

    # Windows only for testing purposes
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

    text = pytesseract.image_to_string(Image.open('title.png'))
    text1 = option_interpreter('cooperative_agreement.png')
    text2 = option_interpreter('grant.png')
    text3 = option_interpreter('education.png')
    text4 = option_interpreter('facilities.png')
    text5 = option_interpreter('research.png')
    text6 = option_interpreter('sdcr.png')
    text7 = option_interpreter('training.png')
    text8 = pytesseract.image_to_string(Image.open('agreement_number.png'))
    text9 = pytesseract.image_to_string(Image.open('supplement_number.png'))
    text10 = pytesseract.image_to_string(Image.open('effective_date.png'))
    text11 = pytesseract.image_to_string(Image.open('completion_date.png'))
    # text12 = pytesseract.image_to_string(Image.open('issued_to_1.png'))
    text13 = pytesseract.image_to_string(Image.open('taxpayer_id.png'))
    text14 = pytesseract.image_to_string(Image.open('cage_num.png'))
    text15 = pytesseract.image_to_string(Image.open('pi_name_phone.png'))
    text16 = pytesseract.image_to_string(Image.open('pi_email.png'))
    text17 = pytesseract.image_to_string(Image.open('project_title.png'))
    text18 = pytesseract.image_to_string(Image.open('purpose.png'))
    text19 = pytesseract.image_to_string(Image.open('period_of_performance.png'))
    text20 = pytesseract.image_to_string(Image.open('aw_previous.png'))
    text21 = pytesseract.image_to_string(Image.open('aw_action.png'))
    text22 = pytesseract.image_to_string(Image.open('aw_cash_share.png'))
    text23 = pytesseract.image_to_string(Image.open('aw_non_cash_share.png'))
    text24 = pytesseract.image_to_string(Image.open('aw_recipient_share.png'))
    text25 = pytesseract.image_to_string(Image.open('aw_total.png'))
    text26 = pytesseract.image_to_string(Image.open('fh_previous.png'))
    text27 = pytesseract.image_to_string(Image.open('fh_action.png'))
    text28 = pytesseract.image_to_string(Image.open('fh_total.png'))
    print(text)
    print(text1)
    print(text2)
    print(text3)
    print(text4)
    print(text5)
    print(text6)
    print(text7)
    print(text8)
    print(text9)
    print(text10)
    print(text11)
    # print(text12)
    print(text13)
    print(text14)
    print(text15)
    print(text16)
    print(text17)
    print(text18)
    print(text19)
    print('\naw')
    print(text20)
    print(text21)
    print(text22)
    print(text23)
    print(text24)
    print(text25)
    print('\nfh')
    print(text26)
    print(text27)
    print(text28)


def option_interpreter(filename):
    """Determines if given image file has a single non-white pixel in it, returns True or False"""
    img = Image.open(filename)
    pixels = img.getdata()
    result = False
    for pixel in pixels:
        if pixel != (0, 0, 0, 0):
            result = True
    return result


if __name__ == "__main__":
    collect_data()
