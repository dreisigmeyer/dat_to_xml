from lxml import etree
import os
import shutil
import subprocess
import xmltodict


magic_validator = etree.XMLParser(
    dtd_validation=True,
    resolve_entities=False,
    encoding='utf-8',
    recover=True)


SECTIONS = {
    'parent_section': '',
    'section': '',
    'subsection': '',
    'PATN': {'parent': 'patent', 'active': False},
    'INVT': {'parent': 'inventors', 'active': False},
    'ASSG': {'parent': 'assignees', 'active': False},
    'PRIR': {'parent': 'foreign_prior', 'active': False},
    'REIS': {'parent': 'reissue', 'active': False},
    'RLAP': {'parent': 'us_related', 'active': False},
    'CLAS': {'parent': 'classifications', 'active': False},
    'UREF': {'parent': 'us_references', 'active': False},
    'FREF': {'parent': 'foreign_references', 'active': False},
    'OREF': {'parent': 'other_references', 'active': False},
    'LREP': {'parent': 'legal_information', 'active': False},
    'PCTA': {'parent': 'pct_information', 'active': False},
    'ABST': {'parent': 'abstract', 'active': False},
    'GOVT': {'parent': 'government_interest', 'active': False},
    'PARN': {'parent': 'parent_case', 'active': False},
    'BSUM': {'parent': 'brief_summary', 'active': False},
    'DRWD': {'parent': 'drawing_description', 'active': False},
    'DETD': {'parent': 'detailed_description', 'active': False},
    'CLMS': {'parent': 'claims_information', 'active': False},
    'DCLM': {'parent': 'design_claim', 'active': False}
}


def reset_sections():
    """
    Puts SECTIONS back to the way it started for a new patent
    """
    global SECTIONS
    SECTIONS['parent_section'] = ''
    SECTIONS['section'] = ''
    SECTIONS['subsection'] = ''
    for key in SECTIONS.keys():
        if 'section' in key:
            continue
        SECTIONS[key]['active'] = False


def new_section(test_str):
    """
    Test to see if a new section of a patent is reached
    """
    global SECTIONS
    test_str = test_str.strip()
    if test_str in SECTIONS.keys():
        if test_str == 'PATN':
            reset_sections()
        parent = SECTIONS[test_str]['parent']
        SECTIONS['section'] = test_str
        SECTIONS['subsection'] = ''
        if not SECTIONS[test_str]['active']:
            SECTIONS['parent_section'] = parent
            SECTIONS[test_str]['active'] = True
            return True, True  # first time we're seeing this section
        else:
            SECTIONS['parent_section'] = parent
            return True, False  # we we're in a previous section
    else:
        return False, False  # not a new section


def new_subsection(test_str):
    """
    To keep track of which subsection we're in for multiline data.
    If it is a subsection the first three characters in test_str will
    determine it.  The 4th and 5th characters are blank.  The 6th
    character is also blank for a continued subsection (like the abstract)
    but we'll send it back for easy concatenation.
    """
    global SECTIONS
    subsec = test_str[:3].strip()
    text = test_str[5:].rstrip()
    if subsec:
        SECTIONS['subsection'] = subsec
        return True, text
    else:
        return False, text


def fix_subsection(section):
    """
    Sometimes there's no subsection: this fixes that.
    """
    global SECTIONS
    sections_with_PAx = ['OREF', 'ABST', 'GOVT', 'PARN', 'BSUM', 'DRWD', 'DETD', 'DCLM']
    if section in sections_with_PAx:
        SECTIONS['subsection'] = 'PAL'  # This PAx is as good as any?


def iconvit_damnit(filename):
    """
    Run iconv and sed on files that are being difficult.
    """
    iconv_args = [
        'iconv',
        '-f utf-8',
        '-t utf-8',
        '-c',
        '-o', filename + '.holder',
        filename]
    subprocess.run(iconv_args)
    mv_args = ['mv', filename + '.holder', filename]
    subprocess.run(mv_args)
    sed_args = 'sed -i "s/\(\x1a\|\x01\)//g" {0}'.format(filename)  # Die SUB die
    subprocess.run(sed_args, shell=True)


def sedit_damnit(filename):
    """
    Some dat files have useless lines to make my life difficult.
    """
    sed_args = 'sed -i -r "/HHHHHT.*APS1.*ISSUE.*/d" {0}'.format(filename)
    subprocess.run(sed_args, shell=True)


def copy_dtds(dest_dir):
    """
    copies the DTD files
    """
    dtd_path = 'DTDs/*'
    cp_args = 'cp -r {0} {1}'.format(dtd_path, dest_dir).strip()
    subprocess.run(cp_args, shell=True)


def create_xml_file(dict_for_xml, wku, out_directory, mod_out_directory):
    """
    Print the dictionary out to an xml file
    """
    inventor_path = './/inventors'
    text_to_file = xmltodict.unparse(dict_for_xml, pretty=True)
    out_file = out_directory + wku + '.xml'
    mod_out_file = mod_out_directory + wku + '.xml'
    with open(out_file, "w") as xml_file:
        xml_file.write(text_to_file)
    sed_args = '''
        sed -i '2i\\<!DOCTYPE patent SYSTEM "early_patent.dtd">\\' {0}
        '''.format(out_file).strip()
    subprocess.run(sed_args, shell=True)
    try:
        tree = etree.parse(out_file, parser=magic_validator)  # valid XML?
    except Exception as e:
        print('===> Invalid XML file for ' + wku)
        print(e)
    try:
        root = tree.getroot()
        inventors_on_patent = root.find(inventor_path)
        if inventors_on_patent is None:  # no inventors to clear
            tree.write(mod_out_file, encoding='UTF-8', xml_declaration=True)
        else:
            inventors_on_patent.clear()
            tree.write(mod_out_file, encoding='UTF-8', xml_declaration=True)
    except Exception as e:
        print("===> Couldn't remove inventors on patent " + wku)
        print(e)


def convert_to_xml(dat_files):
    """
    """
    xml_path = 'xml_files/'
    modified_xml_path = 'modified_xml_files/'
    unzipped_path = 'unzipped_files/'
    for dat_file in dat_files:
        file_name = os.path.basename(dat_file)
        grant_yr = os.path.splitext(file_name)[0]
        out_directory = xml_path + grant_yr
        shutil.rmtree(out_directory, ignore_errors=True)
        os.mkdir(out_directory)
        out_directory += '/'
        mod_out_directory = modified_xml_path + grant_yr
        shutil.rmtree(mod_out_directory, ignore_errors=True)
        os.mkdir(mod_out_directory)
        mod_out_directory += '/'
        copy_dtds(out_directory)
        copy_dtds(mod_out_directory)
        split_args = ['./bash_functions.sh', 'unzip_dat_file', dat_file]
        subprocess.run(split_args)
        unzipped_file = unzipped_path + grant_yr + '.dat'
        iconvit_damnit(unzipped_file)
        sedit_damnit(unzipped_file)
        dict_for_xml = {}
        wku = ''
        with open(unzipped_file) as f:
            for in_line in f:
                try:
                    parent, start_section = new_section(in_line[:4])
                    parent_section = SECTIONS['parent_section']
                    section = SECTIONS['section']
                    if parent:  # take care of new or revisited sections
                        if parent_section == 'patent':
                            if dict_for_xml:
                                create_xml_file(dict_for_xml, wku, out_directory, mod_out_directory)
                            wku = ''
                            dict_for_xml = {}
                            dict_for_xml['patent'] = {}
                        elif start_section:  # new section so a new list
                            dict_for_xml['patent'][parent_section] = {section: []}
                            dict_for_xml['patent'][parent_section][section].append({})
                        else:  # been here before so only need a new dictionary
                            dict_for_xml['patent'][parent_section][section].append({})
                        continue  # no data to place into the XML file
                    # By construction we'll always be working with the last element in a list
                    start_subsection, text = new_subsection(in_line)
                    subsection = SECTIONS['subsection']
                    if not subsection:  # There should be a subsection but there's not...
                        fix_subsection(section)
                        subsection = SECTIONS['subsection']
                        start_subsection = True
                        if not subsection:
                            print('Problem with patent ' + wku + ' : ' + in_line.rstrip())
                    if start_subsection:
                        if parent_section == 'patent':  # putting information into the XML file
                            if subsection == 'WKU':
                                wku = text.strip()[:8]  # there's a check digit at the end
                                dict_for_xml['patent']['WKU'] = wku
                            elif subsection == 'APN':
                                apn = text.strip()[:6]  # there's another check digit
                                dict_for_xml['patent']['APN'] = apn
                            else:
                                dict_for_xml['patent'][subsection] = text.strip()
                        else:
                            dict_for_xml['patent'][parent_section][section][-1][subsection] = text.strip()
                    else:
                        if parent_section == 'patent':
                            dict_for_xml['patent'][subsection] += text
                        else:
                            dict_for_xml['patent'][parent_section][section][-1][subsection] += text
                except Exception as e:
                    print('parent_section : ' + parent_section)
                    print('section : ' + section)
                    print('subsection : ' + subsection)
                    print(str(e) + ' : ' + in_line.rstrip())
                    raise e
        subprocess.run([
            'tar', '-cjf', xml_path + 'pgb' + grant_yr + '.tar.bz2',
            '--directory', xml_path, grant_yr,
            '--remove-files'])
        subprocess.run([
            'tar', '-cjf', modified_xml_path + 'pgb' + grant_yr + '.tar.bz2',
            '--directory', modified_xml_path, grant_yr,
            '--remove-files'])
