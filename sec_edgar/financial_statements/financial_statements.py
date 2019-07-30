import os
import codecs
import traceback
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import zipfile
from pathlib import Path

from sec_edgar.utils import data_log

CURRENT_DIRECTORY = str(Path(__file__).resolve().parents[0])
LOG_FP =  CURRENT_DIRECTORY + '/data/log.json'
VERBOSE = True


def _verify_setup():
    data_fp = CURRENT_DIRECTORY + '/data/'
    unzipped_fp = data_fp + '/unzipped_files/'
    zip_fp = data_fp + '/zip_files/'

    if not os.path.isdir(data_fp): os.mkdir(data_fp)
    if not os.path.isdir(unzipped_fp): os.mkdir(unzipped_fp)
    if not os.path.isdir(zip_fp): os.mkdir(zip_fp)
    if not os.path.isfile(LOG_FP):
        with open(LOG_FP, 'w+') as file_obj:
            file_obj.write('''
                    {
                        "downloaded_files": []
                    }
                '''
            )
            file_obj.close()


def _get_all_links():

    url = 'https://www.sec.gov/dera/data/financial-statement-data-sets.html'
    resp = requests.get(url)

    soup = BeautifulSoup(resp.content, 'html.parser')
    links = soup.find_all('a')
    urls = []
    for link in links:
        href = link.get('href')
        if href is not None and href[-4:] == '.zip':
            urls.append(href)

    return urls


def _extract_new_links(links):

    downloaded_files = data_log.get_logged_item(LOG_FP, 'downloaded_files')

    new_links = []
    for link in links:
        file_name = link.split('/')[-1:][0]
        if not file_name in downloaded_files:
            new_links.append(link)

    return new_links


def _download_links(all_links):
    zip_files_fp = []
    for ix, new_link in enumerate(all_links):
        file_name = new_link.split('/')[-1:][0]
        dest_path = CURRENT_DIRECTORY + '/data/zip_files/' + file_name
        zip_files_fp.append(dest_path)

        if VERBOSE: print('Downloading {}/{} zips'.format(ix + 1, len(all_links)))

        urlretrieve('https://www.sec.gov' + new_link, dest_path)
        data_log.append_log(LOG_FP, 'downloaded_files', [file_name])

    return zip_files_fp


def _unzip_files(unzipped_fp):

    zipped_fp = CURRENT_DIRECTORY + '/data/zip_files/'
    zip_files = os.listdir(zipped_fp)

    unzipped_fps = []
    for zip_file in zip_files:
        unzipped_dest = unzipped_fp + zip_file + '/'
        unzipped_fps.append(unzipped_dest)
        os.mkdir(unzipped_dest)
        zip_obj = zipfile.ZipFile(zipped_fp + zip_file, 'r')
        zip_obj.extractall(unzipped_dest)
        zip_obj.close()

    return unzipped_fps


def _validate_dest_path(dest_path):
    unzipped_fp = CURRENT_DIRECTORY + '/data/unzipped_files/'
    if dest_path:
        try:
            if os.path.isdir(dest_path):
                unzipped_fp = dest_path
            else:
                os.mkdir(dest_path)
                unzipped_fp = dest_path

        except Exception as e:
            print(f"Error validating destination path \nUsing {unzipped_fp} as destination path \nError:\n{e} \n\n{traceback.format_exc()}")
    else:
        print(f'No destination path provided for unzipped files. Files will be unzipped to: \n{unzipped_fp}')
    return unzipped_fp


def _get_files_list(unzipped_fps):
    files_list = []
    for fp in unzipped_fps:
        files = os.listdir(fp)
        for file in files:
            if file[-4:] == '.txt':
                files_list.append(f'{fp}{file}')

    return files_list


def _convert_encoding(file_path):
    with codecs.open(file_path, 'r', encoding='utf8', errors='ignore') as file_obj:
        lines = file_obj.read()

    with codecs.open(file_path, 'w', encoding='utf8') as file_obj:
        file_obj.write(lines)


def _convert_files_list(files_list):

    for ix, fp in enumerate(files_list):
        if VERBOSE: print(f'Converting encoding for file: {ix+1}/{len(files_list)}')
        _convert_encoding(fp)


def _remove_zip_files(zip_files_fp):
    for zip_file in zip_files_fp:
        os.remove(zip_file)




def download(
        dest_path='',
        only_new_files=True,
        reset_download_history=False,
        convert_to_utf8=True,
        verbose=True,
        remove_zip_files=True
):
    """
    :param dest_path: Destination path for unzipped files
    :param only_new_files: Download only new files
    :param reset_download_history: Reset logged history
    :param convert_to_utf8: Convert files to utf8
    :param verbose: Print progress to console
    :param remove_zip_files: Remove downloaded zip files after unzipping
    :return:
    """

    try:
        VERBOSE = verbose

        _verify_setup()

        if reset_download_history:
            data_log.reset_history(LOG_FP, 'downloaded_files')

        all_links = _get_all_links()
        if only_new_files:
            all_links = _extract_new_links(all_links)

        zip_files_fp = _download_links(all_links)

        unzipped_fp = _validate_dest_path(dest_path)
        unzipped_fps = _unzip_files(unzipped_fp)

        if convert_to_utf8:
            files_list = _get_files_list(unzipped_fps)
            _convert_files_list(files_list)

        if remove_zip_files:
            _remove_zip_files(zip_files_fp)

        if VERBOSE:
            if all_links:
                print(f'Finished processing files: ({len(all_links)}) zip files processed')
            else:
                print('No new zip files')

    except Exception as e:
        print(f"Error: \n{e} \n\nTraceback: {traceback.format_exc()}")













