# To Run: python manage.py shell
# >>> exec(open('_import/import_projects.py').read())

import csv
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from summit.apps.projects.models import Project, Location
from summit.libs.auth.models import UserProfile, FederalAgency, Partner, CESUnit

with open('_import/projects.csv') as csv_file:
    # Global vars
    DISCIPLINES = ['None', 'Natural', 'Cultural', 'Social', 'Interdisciplinary']
    SRC_OF_FUNDING = ['None', 'Park Base', 'Region Base', 'NR Project Fund Source', 'I&M Program', 'Other Service-wide Project Source', '80% REA Fee', '20% REA Fee', 'Other NPS Appropriated Source', 'OTHER-non-NPS']

    reader = list(csv.reader(csv_file))

    headers = reader[0]

    f_federal_agency = 0
    f_fiscal_year = 1
    f_p_num = 2
    f_legacy_award_number = 3

    f_partner = 5
    f_location = 6
    f_project_title = 7

    # project_manager
    f_project_manager = 66
    f_project_manager_last = 8
    f_project_manager_first = 9

    # pp_i
    f_pp_i = 65
    f_pp_i_last = 10
    f_pp_i_first = 11

    f_tent_start_date = 12
    f_tent_end_date = 13

    f_discipline = 14

    f_legacy_match_amount = 16

    # budget
    f_budget = 63
    f_budget_backup1 = 17
    f_budget_backup2 = 19

    f_legacy_ca_account_number = 21
    f_legacy_account_number = 22
    f_legacy_area_org = 23

    f_legacy_pwe = 27
    f_description = 28
    f_src_of_funding = 29
    f_legacy_project_products = 30
    f_legacy_received_report_date = 31
    f_legacy_sent_to_tic = 32
    f_notes = 33
    f_final_report = 34

    f_type = 59
    f_youth_vets = 60

    f_sensitive = 62

    f_status_closed = 64

    DEBUG = True

    for row in reader[1:]:
        # federal_agency
        federal_agency = row[f_federal_agency].strip()

        if len(federal_agency) > 0:
            try:
                federal_agency = FederalAgency.objects.get(name=federal_agency)
                if DEBUG: print("get:", federal_agency)
            except ObjectDoesNotExist:
                federal_agency = FederalAgency(name=federal_agency)
                federal_agency.save()
                if DEBUG: print("new:", federal_agency)
        else:
            federal_agency = None

        # fiscal_year
        fiscal_year = row[f_fiscal_year].strip()

        try:
            fiscal_year = int(fiscal_year)
        except ValueError:
            fiscal_year = None
        if DEBUG: print(fiscal_year)

        # p_num
        p_num = row[f_p_num].strip()
        if DEBUG: print(p_num)

        # legacy_award_number
        legacy_award_number = row[f_legacy_award_number].strip()

        # partner
        partner = row[f_partner].strip()

        if len(partner) > 0:
            try:
                partner = Partner.objects.get(name=partner)
                if DEBUG: print("get:", partner)
            except ObjectDoesNotExist:
                partner = Partner(name=partner)
                partner.save()
                if DEBUG: print("new:", partner)
        else:
            partner = None

        # location
        location = str(row[f_location]).strip()

        if len(location) > 0:
            print(location)
            try:
                location = Location.objects.get(abbrv=location)
                if DEBUG: print("get:", location)
            except ObjectDoesNotExist:
                try:
                    location = Location.objects.get(name=location)
                    if DEBUG: print("get:", location)
                except ObjectDoesNotExist:
                    location = Location(name=location)
                    location.save()
                    if DEBUG: print("new:", location)
        else:
            location = None

        # project_title
        project_title = row[f_project_title].strip()

        # project_manager
        project_manager = row[f_project_manager].strip()
        if len(project_manager) > 0:
            project_manager = project_manager.split(' ')
            project_manager_first = project_manager[0]
            project_manager_last = ' '.join(project_manager[1:])
        else:
            project_manager_first = row[f_project_manager_first].strip()
            project_manager_last = row[f_project_manager_last].strip()

        if len(project_manager_first) > 0 and len(project_manager_last) > 0:
            # Grab Profile (get or new)
            try:
                project_manager = UserProfile.objects.get(first_name=project_manager_first, last_name=project_manager_last)
                if DEBUG: print("get:", project_manager)
            except ObjectDoesNotExist:
                project_manager = UserProfile(first_name=project_manager_first, last_name=project_manager_last, assigned_group=federal_agency)
                project_manager.save()
                if DEBUG: print("new:", project_manager)
        else:
            project_manager = None

        # pp_i = principle investigator
        pp_i = row[f_pp_i]
        if len(pp_i) > 0:
            pp_i = pp_i.split(' ')
            pp_i_first = pp_i[0]
            pp_i_last = ' '.join(pp_i[1:])
        else:
            pp_i_first = row[f_pp_i_first]
            pp_i_last = row[f_pp_i_last]

        if len(pp_i_first) > 0 and len(pp_i_last) > 0:
            # Grab Profile (get or new)
            try:
                pp_i = UserProfile.objects.get(first_name=pp_i_first,
                                                          last_name=pp_i_last)
                if DEBUG: print("get:", pp_i)
            except ObjectDoesNotExist:
                pp_i = UserProfile(first_name=pp_i_first, last_name=pp_i_last, assigned_group=partner)
                pp_i.save()
                if DEBUG: print("new:", pp_i)
        else:
            pp_i = None

        # tent_start_date
        tent_start_date = row[f_tent_start_date].strip()

        if len(tent_start_date) > 0:
            # Get datetime format
            tent_start_date = datetime.strptime(tent_start_date, '%Y-%m-%d %H:%M')
            if DEBUG: print(tent_start_date)
        else:
            tent_start_date = None

        # tent_end_date
        tent_end_date = row[f_tent_end_date].strip()

        if len(tent_end_date) > 0:
            # Get datetime format
            tent_end_date = datetime.strptime(tent_end_date, '%Y-%m-%d %H:%M')
            if DEBUG: print(tent_end_date)
        else:
            tent_end_date = None

        # discipline
        discipline = row[f_discipline].strip().capitalize()

        if len(discipline) > 0 and discipline in DISCIPLINES:
            if DEBUG: print(discipline)
            discipline = discipline.upper()

        # legacy_match_amount
        legacy_match_amount = row[f_legacy_match_amount].strip()

        # budget
        budget = row[f_budget].strip().replace('$', '').replace(',', '')
        budget_backup1 = row[f_budget_backup1].strip().replace('$', '').replace(',', '')
        budget_backup2 = row[f_budget_backup2].strip().replace('$', '').replace(',', '')

        try:
            budget = float(budget)
        except ValueError:
            budget = None

        try:
            budget_backup1 = float(budget_backup1)
        except ValueError:
            budget_backup1 = None

        try:
            budget_backup2 = float(budget_backup2)
        except ValueError:
            budget_backup2 = None

        if DEBUG: print(budget, budget_backup1, budget_backup2)

        if budget is None and budget_backup1 is not None:
            budget = budget_backup1
        elif budget is None and budget_backup2 is not None:
            budget = budget_backup2

        if DEBUG: print("budget:", budget)

        # legacy_ca_account_number
        legacy_ca_account_number = row[f_legacy_ca_account_number].strip()

        # legacy_account_number
        legacy_account_number = row[f_legacy_account_number].strip()

        # legacy_area_org
        legacy_area_org = row[f_legacy_area_org].strip()

        # legacy_pwe
        legacy_pwe = row[f_legacy_pwe].strip()

        # description
        description = row[f_description].strip()

        # src_of_funding
        src_of_funding = row[f_src_of_funding].strip()

        if len(src_of_funding) > 0 and src_of_funding in SRC_OF_FUNDING:
            if DEBUG: print(src_of_funding)

        # legacy_project_products
        legacy_project_products = row[f_legacy_project_products].strip()

        # legacy_received_report_date
        legacy_received_report_date = row[f_legacy_received_report_date].strip()

        # legacy_sent_to_tic
        legacy_sent_to_tic = row[f_legacy_sent_to_tic].strip()

        # notes
        notes = row[f_notes].strip()

        # final_report
        final_report = row[f_final_report].strip()

        try:
            final_report = int(final_report)
            if final_report > 0:
                final_report = True
            else:
                final_report = False
        except ValueError:
            final_report = False

        # type
        type = row[f_type].strip()

        # youth_vets
        youth_vets = row[f_youth_vets].strip()

        try:
            youth_vets = int(youth_vets)
            if youth_vets > 0:
                youth_vets = True
            else:
                youth_vets = False
        except ValueError:
            youth_vets = False

        # sensitive
        sensitive = row[f_sensitive].strip()

        try:
            sensitive = int(sensitive)
            if sensitive > 0:
                sensitive = True
            else:
                sensitive = False
        except ValueError:
            sensitive = True

        # status_closed
        status_closed = row[f_status_closed].strip()

        try:
            status_closed = int(status_closed)
            if status_closed > 0:
                status_closed = True
            else:
                status_closed = False
        except ValueError:
            status_closed = False

        if status_closed:
            status = "CLOSED"
        else:
            status = "LEGACY"

        # Setup ces_unit
        cesu_unit = CESUnit.objects.get(pk=1)
        if DEBUG: print(cesu_unit)

        project = Project(
            federal_agency=federal_agency,
            fiscal_year=fiscal_year,
            p_num=p_num,
            legacy_award_number=legacy_award_number,
            partner=partner,
            location=location,
            project_title=project_title,
            project_manager=project_manager,
            pp_i=pp_i,
            tent_start_date=tent_start_date,
            tent_end_date=tent_end_date,
            discipline=discipline,
            legacy_match_amount=legacy_match_amount,
            budget=budget,
            legacy_ca_account_number=legacy_ca_account_number,
            legacy_account_number=legacy_account_number,
            legacy_area_org=legacy_area_org,
            legacy_pwe=legacy_pwe,
            description=description,
            src_of_funding=src_of_funding,
            legacy_project_products=legacy_project_products,
            legacy_received_report_date=legacy_received_report_date,
            legacy_sent_to_tic=legacy_sent_to_tic,
            notes=notes,
            final_report=final_report,
            type=type,
            youth_vets=youth_vets,
            sensitive=sensitive,
            status=status,
            cesu_unit=cesu_unit
        )

        project.save()
