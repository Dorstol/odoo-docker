# -*- coding: utf-8 -*-
import base64
import io
import logging
import re
import zipfile

from odoo import models, fields

_logger = logging.getLogger(__name__)


def sanitize_filename(name):
    """Remove invalid characters from filenames."""
    return re.sub(r'[\\/*?:"<>|]', "_", name)


class ExportSurveyAttachmentWizard(models.TransientModel):
    _name = 'export.survey.attachment.wizard'
    _description = 'Export Survey Attachments Wizard'

    zip_file = fields.Binary('ZIP File', readonly=True)
    zip_filename = fields.Char('File Name', readonly=True)

    def action_export(self):
        active_ids = self.env.context.get('active_ids', [])
        survey_inputs = self.env['survey.user_input'].browse(active_ids)

        # Create an in-memory ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for survey_input in survey_inputs:
                # Get all user input lines (answers) for the survey input
                user_input_lines = survey_input.user_input_line_ids

                # Initialize a flag to check if any files were added
                files_added = False

                for line in user_input_lines:
                    # Check if there are attachments in attachment_ids
                    if line.attachment_ids:
                        # Use sudo() to bypass access rights
                        attachments = line.attachment_ids.sudo()
                        # Folder name — nickname or email or survey_input_ID
                        folder_name = sanitize_filename(
                            survey_input.nickname or survey_input.email or f'survey_input_{survey_input.id}'
                        )
                        question_title = sanitize_filename(line.question_id.title or 'unknown_question')

                        for attachment in attachments:
                            # Get the file name from attachment.name or default to 'uploaded_file'
                            file_name = sanitize_filename(attachment.name or 'uploaded_file')

                            # Get the file data from attachment.datas
                            file_data = base64.b64decode(attachment.datas or b'')

                            if file_data:
                                # Path inside the ZIP file
                                zip_path = f'{folder_name}/{question_title}/{file_name}'

                                # Add the file to the archive
                                zip_file.writestr(zip_path, file_data)

                                _logger.info('Added file %s to ZIP for survey_input ID %d', zip_path, survey_input.id)

                                files_added = True
                            else:
                                _logger.warning('No data in attachment ID %d', attachment.id)
                    else:
                        _logger.info('No attachments for line ID %d', line.id)

                if not files_added:
                    _logger.warning('No files found for survey_input ID %d', survey_input.id)

        # Save the ZIP file in the wizard record
        zip_content = zip_buffer.getvalue()
        zip_buffer.close()
        self.write({
            'zip_file': base64.b64encode(zip_content),
            'zip_filename': 'survey_attachments.zip',
        })

        # Return action to download the file
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model={self._name}&id={self.id}&field=zip_file&filename_field=zip_filename&download=true',
            'target': 'self',
        }
