class ProjectChoices:
    help_text = {
        'p_num': 'Project number. Sometimes not received.',
        'project_title': 'The title of the project',
        'short_summary': 'This field is displayed in "overviews" such as the projects listing page.',
        'description': 'A free-form description of the plugin.',
        'sensitive': 'True if data is sensitive and cannot be revealed to the public.',
        'budget': 'Initial funding amount (USD)',
        'student_support': 'A project may have support from students.',
        'num_of_students': 'Number of students participating in student support.',
        'location': 'A park/location for a project',
        'fed_poc': 'federal point of contact',
        'pp_i': 'Partner Principle Investigator',
        'funding': 'The current/final funding amount',
        'start_date': 'Tentative start date of project',
        'end_date': 'Tentative end date of project',
        'discipline': 'The discipline related to the project',
        'type': 'Type of project implemented',
        'r_d': 'Research and Development fields',
        'tech_rep': 'Agreements Tech Representative if Partner:NPS is selected',
        'alt_coord': 'The Alternate Research Coordinator / CESU Representative',
        'src_of_funding': 'The source of the funding',
        'award_amt': 'The amount that was awarded',
        'field_of_science': 'A specific field of science for the project.',
        'notes': 'General details or specifics that are worth writing down',
        'mod_num': 'An identification for the specific modification made.'
    }

    GRADUATE = 'GRAD'
    UNDERGRADUATE = 'UGRAD'
    BOTH = 'BOTH'
    NONE = 'NONE'
    UNKNOWN = 'UNKNOWN'

    YOUTH = 'YOUTH'
    VETS = 'VETS'

    DRAFTING = 'DRAFT'
    EXECUTED = 'EXECUTED'
    CLOSED = 'CLOSED'

    NATURAL = 'NATURAL'
    CULTURAL = 'CULTURAL'
    SOCIAL = 'SOCIAL'
    INTERDISCIPLINARY = 'INTERDISCIPLINARY'

    EDUCATION = 'EDUCATION'
    RESEARCH = 'RESEARCH'
    TECHNICAL = 'TECHNICAL'
    ASSISTANCE = 'ASSISTANCE'

    PARK = 'PARK'
    REGION = 'REGION'
    SOURCE = 'SOURCE'
    PROGRAM = 'PROGRAM'
    OTHER_PROJECT_SOURCE = 'OTHER_PROJECT_SOURCE'
    REA_FEE_80 = 'REA_FEE_80'
    REA_FEE_20 = 'REA_FEE_20'
    OTHER_NPS_SOURCE = 'OTHER_NPS_SOURCE'
    OTHER = 'OTHER'

    NA = 'NA'
    APPLIED_RESEARCH = 'APPLIED_RESEARCH'
    BASIC_RESEARCH = 'BASIC_RESEARCH'
    R_D = 'R_D'
    DEVELOPMENT = 'DEVELOPMENT'

    ENVIRO_SCI = 'ENVIRO_SCI'
    LIFE_SCI = 'LIFE_SCI'
    MATH_CS = 'MATH_CS'
    PHYSICAL_SC = 'PHYSICAL_SC'
    SOCIAL_SC = 'SOCIAL_SC'

    FUNDED = 'FUNDED'
    NO_COST = 'NO-COST'
    ADMIN = 'ADMIN'
    FUNDED_EXT = 'FUNDED_EXT'
    FUNDED_ADMIN = 'FUNDED_ADMIN'
    NO_COST_EXT_ADMIN = 'NO_COST_EXT_ADMIN'

    #
    # ES - Atmospheric Sciences,
    # ES - Geological Sciences,
    # ES – Oceanography,
    # ES - Environmental Sciences NEC,
    # LS - Biological (excl.Environmental)
    # LS - Environmental Biology,
    # LS - Agricultural Science,
    # LS - Medical Science,
    # LS - Life Science NEC
    # ES_AS = 'ES_AS'
    # ES_GS = 'ES_GS'
    # ES_O = 'ES_O'
    # ES_ES = 'ES_ES'
    # LS_BI = 'LS_BI'
    # LS_EB = 'ES_EB'

    STUDENT_SUPPORT = (
        (NONE, 'None'),
        (GRADUATE, 'Graduate'),
        (UNDERGRADUATE, 'Undergraduate'),
        (BOTH, 'Graduate and Undergraduate'),
        (UNKNOWN, 'Unknown'),
    )
    VET_SUPPORT = (
        (NONE, 'None'),
        (YOUTH, 'Youth/Young Adults'),
        (VETS, 'Veterans'),
        (BOTH, 'Youth/Young Adults and Veterans'),
    )
    STATUS = (
        (DRAFTING, 'Drafting'),
        (EXECUTED, 'Executed'),
        (CLOSED, 'Closed')
    )
    DISCIPLINE = (
        (NONE, 'None'),
        (NATURAL, 'Natural'),
        (CULTURAL, 'Cultural'),
        (SOCIAL, 'Social'),
        (INTERDISCIPLINARY, 'Interdisciplinary')
    )
    TYPE = (
        (NONE, 'None'),
        (EDUCATION, 'Education'),
        (RESEARCH, 'Research'),
        (TECHNICAL, 'Technical'),
        (ASSISTANCE, 'Assistance')
    )
    SOURCE_OF_FUNDING = (
        (NONE, 'None'),
        (PARK, 'Park Base'),
        (REGION, 'Region Base'),
        (SOURCE, 'NR Project Fund Source'),
        (PROGRAM, 'I&M Program'),
        (OTHER_PROJECT_SOURCE, 'Other Service-wide Project Source'),
        (REA_FEE_80, '80% REA Fee'),
        (REA_FEE_20, '20% REA Fee'),
        (OTHER_NPS_SOURCE, 'Other NPS Appropriated Source'),
        (OTHER, 'OTHER-non-NPS')
    )
    R_D_TYPE = (
        (NA, 'NA (TA or Educ)'),
        (APPLIED_RESEARCH, 'Applied Research'),
        (BASIC_RESEARCH, 'Basic Research'),
        (R_D, 'Research and Development'),
        (DEVELOPMENT, 'Development')
    )
    FIELD_OF_SCIENCE = (
        (NONE, 'None'),
        (ENVIRO_SCI, 'Environmental Sciences'),
        (LIFE_SCI, 'Life Sciences'),
        (MATH_CS, 'Math & Computer Sciences'),
        (PHYSICAL_SC, 'Physical Sciences'),
        (SOCIAL_SC, 'Social Sciences')
    )
    MOD_TYPE = (
        (NONE, 'None'),
        (FUNDED, 'Funded'),
        (NO_COST, ' No-cost Time Extension'),
        (ADMIN, 'Administrative'),
        (FUNDED_EXT, 'Funded & Time Extension'),
        (FUNDED_ADMIN, 'Funded & Administrative'),
        (NO_COST_EXT_ADMIN, 'No-cost Time Extension & Administrative')
    )
