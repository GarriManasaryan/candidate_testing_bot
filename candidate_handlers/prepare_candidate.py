from services.google_service import *
import uuid

class CandidateSetUp():

    def __init__(self):
        self.gsr = GoogleServiceHandler()

    def get_candidate_data(self, email):
        df_all_candidates, worksheet_canidate = self.gsr.get_google_sheet_df()
        self.all_tokens = set(df_all_candidates['token'])

        df_candidate = df_all_candidates[df_all_candidates['email'] == email]

        if not df_candidate.empty:
            self.candidate_info_dict = df_candidate.to_dict('records')[0]
            status = 'ok'

        else:
            status = 'not_found'

        return status

    def gen_token(self):
        """
        deprecated, implementation in google scripts for now
        """
        uuid_full = str(uuid.uuid4())
        uuid_first_chunk = uuid_full[:8]
        uuid_last_chunk = uuid_full[19:]

        l_name = str(self.candidate_info_dict.get('Last_name', 'l_name')).replace(' ', '').lower()
        f_name = str(self.candidate_info_dict.get('First_name', 'f_name')).replace(' ', '').lower()
        token = '-'.join(['cand', f_name, uuid_first_chunk, l_name, uuid_last_chunk])
        return token

    def generate_candidate_token(self):
        token = self.gen_token()

        while token in self.all_tokens:
            token = self.gen_token()

        return token

    def download_candidate_task(self):
        try:
            docx_file_id_in_drive = self.candidate_info_dict.get('Link_to_docx_task').replace(' ', '').split('/')[-2]
            self.gsr.docs_downloader_from_drive(docx_file_id_in_drive)
            status = 'ok'

        except:
            status = 'not_found'
