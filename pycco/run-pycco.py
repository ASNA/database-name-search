# Generate AVR annotated code.

# The modified Pycco Python file is here:
# C:\Users\roger\AppData\Local\Programs\Python\Python38\Lib\site-packages\pycco\main.py
# It leaves //-- comments in the code.

import glob, os, shutil, re

def create_index_file(template_filename, files):
    template_contents = read_file(template_filename)
    index_list = create_index_list(files)
    template_contents = template_contents.replace('{{directory}}', index_list)
    write_file('./docs/pycco-index.html', template_contents)

def write_file(filename, contents):
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(contents)

def read_file(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        return f.read()

def delete_folder_contents(folder):
    #  Save template file contents.
    directory_template_contents = read_file('./docs/__index.template.html')

    for root, dirs, files in os.walk(folder):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    # Restore template file contents.
    write_file('./docs/__index.template.html', directory_template_contents)            

def create_index_list(files):
    index_list = ''
    anchor_tags = []
    template = '{filename}|<li><a href="{url}">{filename}</a></li>'
    root_name = ''
    for file in files:
        if '\\' in file:
            root_name = ''
        else:            
            root_name = '_ROOT_/'
        filename_to_show = root_name + file.replace('\\', '/').lower()
        tag = template.format(url=file + '.html', filename=filename_to_show)
        anchor_tags.append(tag)
    anchor_tags.sort()

    for anchor_tag in anchor_tags:
        anchor_tag = anchor_tag.replace('_ROOT_/', '')
        index_list += re.sub(r'^.*\|', '', anchor_tag)

    return index_list
    
if __name__ == '__main__':  
    if not os.path.isdir('../docs'):    
        os.mkdir('../docs')        
    if not os.path.isfile('../docs/__index.template.html'):
        shutil.copy('index.template.html', '../docs/__index.template.html')        

    # This program needs to run in the context of the root directory.
    os.chdir('..')
    
    # places to look for source files
    searches = ('global.asax', 'web.config', '*.aspxfff', '**/*.aspx', '**/*.vr', 'app_codcccce/*.vr' )
    # source file ending names to ignore.
    ignored_files = ('^.*designer.vr', '^.*assemblyinfo.vr')        

    files = []
    for search in searches:
        files.extend(glob.glob(search, recursive=True)) 

    purged_files = []
    for file in files:
        include_file = True
        for ignored_file in ignored_files:
            pattern = re.compile(ignored_file + '$', re.I)
            if re.match(pattern, file):
                print(f'Ignored file = {file}')
                include_file = False
                break
        if include_file:
            purged_files.append(file)       

    delete_folder_contents('./docs')

    create_index_file(template_filename='./docs/__index.template.html', files=purged_files)

    for file in purged_files:
        cmd = f'pycco {file} -d ./docs -l javascript -p'
        os.system(cmd)

    shutil.copy("pycco/pycco.css", './docs/')    
