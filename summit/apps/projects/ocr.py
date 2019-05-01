from wand.image import Image as Img
from PIL import Image
import pytesseract
import os
from celery import current_task


def collect_data(filename):
    """Gets data from a Grant Cooperative Agreement, returns dict"""
    with Img(filename=filename, resolution=300) as img:
        img.save(filename='test.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 5})

        img = Image.open('test-0.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 10})

        options = ['cooperative_agreement', 'grant',
                   'education', 'facilities', 'research', 'sdcr', 'training']

        # The input for img.crop is the xy coordinates of two points to form box to be cropped
        # OPTION: Cooperative Agreement or Grant
        cooperative_agreement = img.crop((2096, 208, 2128, 240))
        cooperative_agreement.save('cooperative_agreement.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 15})

        grant = img.crop((2098, 306, 2130, 336))
        grant.save('grant.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 20})

        # OPTION: Education, Facilities, Research, SDCR, Training
        education = img.crop((461, 444, 491, 470))
        education.save('education.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 25})

        facilities = img.crop((895, 444, 926, 470))
        facilities.save('facilities.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 30})

        research = img.crop((1280, 444, 1310, 470))
        research.save('research.png')
        sdcr = img.crop((1736, 444, 1764, 470))
        sdcr.save('sdcr.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 35})

        training = img.crop((2094, 444, 2122, 470))
        training.save('training.png')

        # Non-options
        pictures = ['title', 'agreement_number', 'supplement_number', 'effective_date',
                    'completion_date', 'taxpayer_id', 'cage_num', 'pi_name_phone', 'pi_email', 'project_title',
                    'purpose', 'period_of_performance', 'aw_previous', 'aw_action', 'aw_cash_share',
                    'aw_non_cash_share', 'aw_recipient_share', 'aw_total', 'fh_previous', 'fh_action', 'fh_total']

        # PICTURE: Document Title
        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 40})

        doc_title = img.crop((80, 125, 2030, 420))
        doc_title.save('title.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 45})

        # 1. Grant/Cooperative Agreement Number
        agreement_number = img.crop((85, 592, 984, 634))
        agreement_number.save('agreement_number.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 50})

        # 2. Supplement Number
        # supplement_number = img.crop((1006, 592, 1566, 634))
        # supplement_number.save('supplement_number.png')

        # 3. Effective Date
        effective_date = img.crop((1579, 592, 2028, 634))
        effective_date.save('effective_date.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 55})

        # 4. Completion Date
        completion_date = img.crop((2049, 592, 2443, 634))
        completion_date.save('completion_date.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 60})

        # 5. Issued To - Name/Address of Recipient(No., Street, City/County, State, Zip)
        # 6. Issued By - Mailing Address

        # 7. Taxpayer Identification No. (TIN)
        # taxpayer_id = img.crop((85, 1040, 1145, 1075))
        # taxpayer_id.save('taxpayer_id.png')

        # 8. Commercial & Government Entity (CAGE) No.
        # cage_num = img.crop((80, 1140, 1145, 1175))
        # cage_num.save('cage_num.png')

        # 9. Principal Investigator/Organization's Project or Program MGR. (Name & Phone)
        # pi_name_phone = img.crop((1165, 1060, 2460, 1110))
        # pi_name_phone.save('pi_name_phone.png')
        # pi_email = img.crop((1165, 1115, 2460, 1170))
        # pi_email.save('pi_email.png')

        # 10. Research, Project, or Program Title
        project_title = img.crop((79, 1223, 2460, 1325))
        project_title.save('project_title.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 65})

        # 11. Purpose
        purpose = img.crop((79, 1378, 2460, 1480))
        purpose.save('purpose.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 70})

        # 12. Period of Performance (Approximately)
        # period_of_performance = img.crop((79, 1532, 2460, 1580))
        # period_of_performance.save('period_of_performance.png')

        # 13A. Award History - Previous, This Action, Cash Share, Non-Cash Share, Recipient Share, Total
        # aw_previous = img.crop((516, 1640, 1240, 1679))
        # aw_previous.save('aw_previous.png')
        # aw_action = img.crop((516, 1688, 1240, 1727))
        # aw_action.save('aw_action.png')
        # aw_cash_share = img.crop((516, 1735, 1240, 1779))
        # aw_cash_share.save('aw_cash_share.png')
        # aw_non_cash_share = img.crop((516, 1786, 1240, 1829))
        # aw_non_cash_share.save('aw_non_cash_share.png')
        # aw_recipient_share = img.crop((516, 1837, 1240, 1879))
        # aw_recipient_share.save('aw_recipient_share.png')
        aw_total = img.crop((516, 1888, 1240, 1929))
        aw_total.save('aw_total.png')

        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': 75})

        # 13B. Funding History - Previous, This Action, Total
        # fh_previous = img.crop((1720, 1640, 2465, 1679))
        # fh_previous.save('fh_previous.png')
        # fh_action = img.crop((1720, 1688, 2465, 1727))
        # fh_action.save('fh_action.png')
        # fh_total = img.crop((1720, 1735, 2465, 1780))
        # fh_total.save('fh_total.png')

        # 14. Accounting and Appropriation Data

        # 15. Points of Contact

    # Windows only for testing purposes
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

    pdf_field_text = {}

    for picture in pictures:
        try:
            pdf_field_text[picture] = pytesseract.image_to_string(Image.open(picture + '.png'))
            os.remove(picture + '.png')
        except FileNotFoundError:
            print(picture + '.png not found\n')

    current_task.update_state(state='PROGRESS',
                              meta={'process_percent': 80})

    for option in options:
        try:
            pdf_field_text[option] = option_interpreter(option + '.png')
            os.remove(option + '.png')
        except FileNotFoundError:
            print(option + '.png not found\n')

    current_task.update_state(state='PROGRESS',
                              meta={'process_percent': 85})

    try:
        os.remove('test-0.png')
    except FileNotFoundError:
        print('test.png not found\n')

    return pdf_field_text


def option_interpreter(filename):
    """Determines if given image file has a single non-white pixel in it, returns True or False"""
    img = Image.open(filename)
    pixels = img.getdata()
    result = False
    for pixel in pixels:
        if pixel != (0, 0, 0, 0):
            result = True
    return result
