import glob
import os
import sys
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import *
from tkinter import ttk
from cleaner import *

try:
    from GUI import *
    from validate_email import validate_email
except:
    os.system('pip install Pillow')
    os.system('pip install validate_email')
    # Restart
    os.execl(sys.executable, 'filter.py', *sys.argv)

print('-------------------------------Starting the filtering of the mailing data--------------------------------------')
print()
print()
# Creating main result folder
if not os.path.isdir('filter_result'):
    os.mkdir('filter_result')

if not os.path.isdir('clean_result'):
    os.mkdir('clean_result')

result_path_saver = ''
tmp_data_saver = []
result_saver = []
keep = True
percent = 0
size = 0


# Function that starts the job
def execute_filter_action(arg, start=0):
    button.configure(state=DISABLED)
    pause.configure(state=NORMAL)
    global result_path_saver
    global percent
    file = arg
    arg = arg[arg.rindex('/') + 1:]
    # ------------------------------------------------------------------------------------------------------------------
    # Initialising global working vars
    saver = []
    counter = 0
    duplicated = dict()
    path = 'filter_result/' + arg[0:arg.index('.')]
    result_path_saver = path
    non_valid_emails = []
    if os.path.isfile(path + '/stats/invalid_emails.txt'):
        with open(path + '/stats/invalid_emails.txt') as f:
            non_valid_emails = f.read().split('\n')
    stats = dict()
    if os.path.isfile(path + '/tmp_stats'):
        for line in open(path + '/tmp_stats'):
            data = line.split('=')
            stats[data[0]] = int(data[1])
    # ------------------------------------------------------------------------------------------------------------------
    # Creating folder for the specified selected file
    if not os.path.isdir(path):
        os.mkdir(path)
    # ------------------------------------------------------------------------------------------------------------------
    # Creating result folder
    if not os.path.isdir(path + '/result'):
        os.mkdir(path + '/result')
    # ------------------------------------------------------------------------------------------------------------------
    # Looping inside data file
    for d in open(file):
        # See if a line is void
        if d == '\n':
            continue
        # See if the counter is started
        if counter < start:
            counter += 1
            console.configure(text='Resuming ' + str(counter))
            continue
        counter += 1
        while not keep:
            console.configure(text='Paused')
            root.update()
        if counter > size or start >= size:
            break
        percent = (counter * 100) / size
        print('|-> attempt filtering n°:' + str(counter))
        console.configure(text=str(counter) + ' | ' + str(int(percent)) + ' %')
        button.config(text='Filtering ' + str(int(percent)) + ' %')
        root.update()
        info = d.split(':')
        email = info[0]
        part = email[email.index('@'):]
        brand = part[1:part.rindex('.')].lower()
        # Validating email syntactical data
        if not validate_email(email) and email not in non_valid_emails:
            non_valid_emails.append(email)
            continue
        # Validating email semantic data
        if '.edu' in email and email not in non_valid_emails:
            non_valid_emails.append(email)
            continue
        # Validating email duplication
        if email not in saver:
            duplicated[brand] = 0
            saver.append(email)
        else:
            duplicated[brand] += 1
            continue
        # Validating email brand duplication
        if brand not in stats.keys():
            stats[brand] = 0
        stats[brand] += 1
        # Writing data to file
        with open(path + '/result/' + brand + '.txt', 'a') as emails:
            emails.write(email.strip() + '\n')
        # Saving data to vars
        with open(path + '/tmp', 'w+') as tmp_file:
            tmp_file.write(str(counter))
        # --------------------------------------------------------------------------------------------------------------
        # Creating stats folder
        if not os.path.isdir(path + '/stats'):
            os.mkdir(path + '/stats')
        # Creating stats file with initialisation
        initFile(path + '/stats/stats.txt')
        with open(path + '/stats/stats.txt', 'a+') as stats_file:
            stats_file.write('-----------------------------STATS-----------------------------\n')
            # All data stats
            stats_file.write('|-> All = ' + str(counter) + '\n')
            # Sort data
            sort_orders = sorted(stats.items(), key=lambda x: x[1], reverse=True)
            # Data by brand
            for i in sort_orders:
                result_saver.append(i[0] + ':' + str(i[1]))
                stats_file.write('|->' + i[0] + '=' + str(i[1]) + '\n')
            # Duplicating stats
            stats_file.write('-------------------------Duplicated-----------------------------\n')
            for k, v in duplicated.items():
                if v != 0:
                    stats_file.write('|->' + k + '=' + str(v) + '\n')
            # Non Valid Emails
            stats_file.write('-------------------------NonValidEmail---------------------------\n')
            stats_file.write('|-> All = ' + str(len(non_valid_emails)) + '\n')
            initFile(path + '/stats/invalid_emails.txt')
            with open(path + '/stats/invalid_emails.txt', 'a+') as nve:
                i = 0
                for e in non_valid_emails:
                    if i == 0:
                        nve.write(e)
                    else:
                        nve.write('\n' + e)
                    i = 1
            # Save stats
            initFile(path + '/tmp_stats')
            with open(path + '/tmp_stats', 'a+') as tmp_stats_file:
                for k, v in stats.items():
                    tmp_stats_file.write(k + '=' + str(v) + '\n')

    print('|-> Finished :)')
    button.configure(text='Filter', state=NORMAL)
    result.configure(state=NORMAL)
    pause.configure(state=DISABLED)
    actions.update()
    os.system('notepad ' + path + '/stats/stats.txt')
    root.update()


def accept_file(event):
    global tmp_data_saver
    global size
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    if filename == '':
        return
    if filename[filename.rindex('.') + 1:] != 'txt':
        showerror('Loading error', 'Chosen file should be a text file = file.txt')
    else:
        size = sizeFile(filename)
        button.config(text='Progress ' + str(percent) + ' %')
        root.update()
        if os.path.isfile('filter_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')] + '/tmp'):
            with open('filter_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')] + '/tmp') as tmp_file:
                start = int(tmp_file.read())
                if start != 0:
                    ask = askquestion('Data',
                                      'Data of this file is already in queue do you want to resume it ?')
                    if ask == 'yes':
                        execute_filter_action(filename, start)
                    else:
                        wrp = 'filter_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')]
                        os.system('rd /s /q ' + wrp.replace('/', '\\'))
                        execute_filter_action(filename, 0)
        else:
            start = 0
            execute_filter_action(filename, start)


def toggle(event):
    if pause['state'] != NORMAL:
        return
    global keep
    keep = not keep
    if keep:
        pause.config(text='Pause')
        result.configure(state=DISABLED)
    else:
        pause.config(text='Resume')
        result.configure(state=NORMAL)


def initFile(filename):
    with open(filename, 'w+') as file:
        pass


def sizeFile(filename):
    counter = 0
    for line in open(filename):
        counter += 1
    return counter


def cleanBounce(event):
    global result_path_saver
    showinfo('Clean',
             'Note that you should chose a filtered data in order to clean the bounce from it ! We recommend you to use the data resulted in filter_result folder')
    filename = askopenfilename(initialdir=result_path_saver + '/result')
    if filename == '':
        return
    size1 = sizeFile(filename)
    success_counter = 0
    bounce_counter = 0
    result_path_saver = 'clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')]
    # create bounce folder
    if not os.path.isdir('clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')]):
        os.mkdir('clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')])
    if not os.path.isdir('clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')]):
        os.mkdir('clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')])
    print("-------Debut---------")
    pause.configure(state=NORMAL)
    result.configure(state=DISABLED)
    counter = 0
    start = 0
    clean.configure(state=DISABLED)
    if os.path.isfile('clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')] + '/tmp'):
        with open('clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')] + '/tmp') as tmp_file:
            start = int(tmp_file.read())
    if start != 0:
        ask = askquestion('Clean', 'Cleaning operation already started do you want to resume it ?')
        if ask != 'yes':
            start = 0
            os.system('rd /s /q ' + result_path_saver.replace('/', '\\'))
            os.mkdir(result_path_saver)
    # Init of counters
    if os.path.isfile('clean_result/' + filename[
                                                 filename.rindex('/') + 1:filename.rindex('.')] + '/success.txt'):
        success_counter = sizeFile('clean_result/' + filename[
                                                 filename.rindex('/') + 1:filename.rindex('.')] + '/success.txt')
    if os.path.isfile('clean_result/' + filename[
                                                 filename.rindex('/') + 1:filename.rindex('.')] + '/bounce.txt'):
        bounce_counter = sizeFile('clean_result/' + filename[
                                                 filename.rindex('/') + 1:filename.rindex('.')] + '/bounce.txt')
    for row in open(filename):
        while not keep:
            console.configure(text='Paused')
            root.update()
        if counter < start:
            console.configure(text='Resuming ' + str(counter))
            root.update()
            counter += 1
            continue
        counter += 1
        percent1 = (counter * 100)/size1
        clean.configure(text='Cleaning ' + str(int(percent1)) + ' %')
        root.update()
        if emailsyntax(row.strip()):
            try:
                eml = email(row.strip())
                if eml.valideEmail() == True:
                    fc = open('clean_result/' + filename[
                                                 filename.rindex('/') + 1:filename.rindex('.')] + '/success.txt',
                              'a+')
                    print("-------succes----------")
                    console.config(text=row, fg='green')
                    print(row)
                    fc.write(row.strip() + '\n')
                    fc.close()
                    success_counter += 1
                else:
                    fb = open('clean_result/' + filename[
                                                 filename.rindex('/') + 1:filename.rindex('.')] + '/bounce.txt',
                              'a+')
                    print("-------bounce---------")
                    console.config(text=row, fg='red')
                    print(row)
                    fb.write(row.strip() + '\n')
                    fb.close()
                    bounce_counter += 1
                root.update()
            except:
                pass
            with open('clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')] + '/tmp', 'w+') as tmp_file:
                tmp_file.write(str(counter))
            # Save stats
            with open('clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')] + '/stats.txt',
                      'w+') as stats_file:
                stats_file.write('All emails = ' + str(counter) + '\n')
                stats_file.write('Success emails = ' + str(success_counter) + '\n')
                stats_file.write('Bounce emails = ' + str(bounce_counter) + '\n')
    print("-------Fin---------")
    pause.configure(state=DISABLED)
    result.configure(state=NORMAL)
    clean.configure(text='Clean', state=NORMAL)
    error = 0
    if os.path.isfile('clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')] + '/success.txt'):
        os.system(
        'notepad clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')] + '/success.txt')
    else:
        error += 1
    if os.path.isfile('clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')] + '/bounce.txt'):
        os.system('notepad clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')] + '/bounce.txt')
    else:
        error += 1
    if error == 2:
        showerror('Clean', 'Sorry but the app was unable to clean the selected brand, please try it on brands such as gmail, yahoo...')
    if os.path.isfile('clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')] + '/stats.txt'):
        os.system('notepad clean_result/' + filename[filename.rindex('/') + 1:filename.rindex('.')] + '/stats.txt')
    root.update()


def clearAll(event):
    ask = askquestion('Clear', 'Are you sure you want to clear all data ?')
    if ask == 'yes':
        files = glob.glob('filter_result/*')
        for file in files:
            if os.path.isdir(file):
                os.system('rd /s /q ' + file)
    ask = askquestion('Clear', 'Do you want to clear the cleaned data too ?')
    if ask == 'yes':
        files = glob.glob('clean_result/*')
        for file in files:
            if os.path.isdir(file):
                os.system('rd /s /q ' + file)


def openResult(event):
    if result['state'] != NORMAL:
        return
    if os.path.isdir(result_path_saver):
        os.system('start ' + result_path_saver.replace('/', '\\'))


def quit(event):
    root.destroy()
    sys.exit(0)


if __name__ == '__main__':
    root = Root('Max Filter By HMZ')
    root.config(bg=B[3])
    escape_exit(root)
    root.center(400, 600)
    image = ImageTk.PhotoImage(Image.open('pictures/title.png'))
    title = BLImagedTitle(root, image, 'Max Filter')
    console = Label(bg='black', fg=F[1], height=2, width=80, text='Standing By', font=('Agency', 20))
    actions = BLbuttons(root, 'Filter', 'Clean')
    actions.buttons[0].bind('<Button-1>', accept_file)
    actions.buttons[1].bind('<Button-1>', cleanBounce)
    actions.exbutton.destroy()
    ownership = Label(root, text='Max Filter v1.0 By HMZ | Contact us at alaouiismaili28@gmail.com', fg=F[0],
                      bg='black', width=100)
    button = actions.buttons[0]
    clean = actions.buttons[1]
    pause = BLbutton(root, 'Pause')
    pause.config(width=20, state=DISABLED)
    pause.bind('<Button-1>', toggle)
    result = BLbutton(root, 'Show Result')
    result.config(width=20, state=DISABLED)
    result.bind('<Button-1>', openResult)
    clear = BLbutton(root, 'Clear')
    clear.config(width=20)
    clear.bind('<Button-1>', clearAll)
    exb = BLbutton(root, 'Quit')
    exb.unbind('<Enter>')
    exb.unbind('<Leave>')
    exb.configure(width=20, fg='white', bg='red')
    exb.bind('<Button-1>', quit)
    title.pack(side=TOP)
    actions.pack(pady=5)
    console.pack(pady=10)
    pause.pack(pady=5)
    result.pack()
    clear.pack(pady=5)
    exb.pack()
    ownership.pack(side=BOTTOM)
    root.mainloop()
