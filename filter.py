import os
import sys
from GUI import *
from validate_email import validate_email
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import *

print('-------------------------------Starting the filtering of the mailing data--------------------------------------')
print()
print()
# Creating main result folder
if not os.path.isdir('filter_result'):
    os.mkdir('filter_result')

result_path_saver = ''
keep = True

with open('tmp') as resume_file:
    resume = resume_file.read()


# Function that starts the job
def execute_filter_action(arg, start=0):
    toggleButton.config(state=NORMAL)
    global result_path_saver
    file = arg
    arg = arg[arg.rindex('/') + 1:]
    # ------------------------------------------------------------------------------------------------------------------
    # Initialising global working vars
    email_brands = []
    non_valid_emails = []
    stats = dict()
    saver = []
    counter = 0
    duplicated = dict()
    path = 'filter_result/' + arg[0:arg.index('.')]
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
        while not keep:
            console.configure(text='Paused')
            root.update()
        if counter < start:
            counter += 1
            console.configure(text='Resuming ' + str(counter))
            continue
        print('|-> attempt filtering n°:' + str(counter))
        console.configure(text=counter)
        root.update()
        info = d.split(':')
        email = info[0]
        part = email[email.index('@'):]
        brand = part[1:part.rindex('.')].lower()
        # Validating email syntactical data
        if not validate_email(email):
            non_valid_emails.append(email)
            continue
        # Validating email semantic data
        if '.edu' in email:
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
        if brand not in email_brands:
            stats[brand] = 0
            email_brands.append(brand)
        # Writing data to file
        result_path_saver = path
        with open(path + '/result/' + brand + '.txt', 'a') as emails:
            emails.write(email + '\n')
        # Saving data to vars
        counter += 1
        with open('tmp', 'w+') as tmp_file:
            tmp_file.write(arg[0:arg.index('.')] + '=' + str(counter))
        stats[brand] += 1
    # ------------------------------------------------------------------------------------------------------------------
    # Creating stats folder
    if not os.path.isdir(path + '/stats'):
        os.mkdir(path + '/stats')
    # Creating stats file
    with open(path + '/stats/stats.txt', 'a') as stats_file:
        stats_file.write('-----------------------------STATS-----------------------------\n')
        # All data stats
        stats_file.write('|-> All = ' + str(counter) + '\n')
        # Sort data
        sort_orders = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        # Data by brand
        for i in sort_orders:
            stats_file.write('|->' + i[0] + '=' + str(i[1]) + '\n')
        # Duplicating stats
        stats_file.write('-------------------------Duplicated-----------------------------\n')
        for k, v in duplicated.items():
            if v != 0:
                stats_file.write('|->' + k + '=' + str(v) + '\n')
        # Non Valid Emails
        stats_file.write('-------------------------NonValidEmail---------------------------\n')
        stats_file.write('|-> All = ' + str(len(non_valid_emails)) + '\n')
        with open(path + '/stats/invalid_emails.txt', 'a') as nve:
            for e in non_valid_emails:
                nve.write(e + '\n')

    print('|-> Finished :)')
    with open('tmp', 'w+') as tmp_file:
        tmp_file.write('0')
    os.system('notepad ' + path + '/stats/stats.txt')
    statsButton.config(state=NORMAL)
    toggleButton.config(state=DISABLED)
    root.update()


def accept_file(event):
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    if filename[filename.rindex('.') + 1:] != 'txt':
        showerror('Loading error', 'Chosen file should be a text file = file.txt')
    else:
        data = resume.split('\n')
        start = 0
        for d in data:
            v = d.split('=')
            tv = filename[filename.rindex('/') + 1:filename.rindex('.')]
            if v[0] == tv:
                start = int(v[1])
        execute_filter_action(filename, start)


def quit(event):
    root.destroy()
    sys.exit(0)


def result(event):
    os.system('notepad ' + result_path_saver + '/stats/stats.txt')


def toggle(event):
    global keep
    keep = not keep


if __name__ == '__main__':
    try:
        file_as_arg = sys.argv[1]
        execute_filter_action(file_as_arg)
    except:
        root = Root('HMZ Filter')
        root.center(400, 650)
        image = ImageTk.PhotoImage(Image.open('pictures/title.png'))
        title = BLImagedTitle(root, image, 'Max Filter')
        console = Label(bg='black', fg='green', height=2, width=80, text='Standing By', font=('Courier', 20))
        button = BLbutton(root, 'Choose Data File')
        button.config(width=30)
        statsButton = BLbutton(root, 'Show Result')
        statsButton.config(width=30, state=DISABLED)
        toggleButton = BLbutton(root, 'Toggle (Pause/Run)')
        toggleButton.config(width=30, state=DISABLED)
        exitButton = BLbutton(root, 'Exit')
        exitButton.config(width=30)
        title.pack(side=TOP)
        console.pack()
        button.pack(pady=20)
        statsButton.pack()
        toggleButton.pack(pady=20)
        exitButton.pack()
        button.bind('<Button-1>', accept_file)
        statsButton.bind('<Button-1>', result)
        toggleButton.bind('<Button-1>', toggle)
        exitButton.bind('<Button-1>', quit)
        root.mainloop()
