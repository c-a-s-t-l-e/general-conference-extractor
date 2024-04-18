# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_Data_Output.ipynb.

# %% auto 0
__all__ = ['save_talk_text']

# %% ../nbs/02_Data_Output.ipynb 3
import os
def save_talk_text(output_folder, talk):
    """Saves the text of a talk to a file."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    filename = f"{talk.metadata.get('title', 'unknown_title').replace(' ', '_')}.txt"
    file_path = os.path.join(output_folder, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(talk.text)
    
    # Update metadata with the filename for reference
    talk.metadata['filename'] = filename
    print(talk.metadata)
    return talk.metadata
