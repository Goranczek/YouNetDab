import time
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
from pathlib import Path
import json
import uuid
import sys
from traceback import print_exc
from datetime import datetime
import yaml
import logging.handlers
from kafka import KafkaProducer
from main import kokos
from bteq.bteq import bteq_params


logger = logging.getLogger(__name__)

class Window(object):

    def __init__(self, root):
        self.full_dict = {"files": list()}
        self.root = root
        self.deploy_dir = ""
        self.deploy_clean = ""
        self.root.wm_title("CI Teradata")
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

        self.root.iconbitmap(r'{}\icon.ico'.format(self.dir_path))

        # root label
        self.l1 = Label(root, text="Files")

        login_holder = StringVar()
        self.login = Label(self.root, text="Username")
        self.login.grid(row=0, column=0)
        self.textfield_login = ttk.Entry(self.root, textvariable=login_holder)
        self.textfield_login.grid(row=0, column=1)

        pass_holder = StringVar()
        self.password = Label(self.root, text="Password")
        self.password.grid(row=1, column=0)
        self.textfield_pass = ttk.Entry(self.root, textvariable=pass_holder)
        self.textfield_pass.config(show="*")
        self.textfield_pass.grid(row=1, column=1)

        # root combobox
        loader_tmp = StringVar()
        self.cb1 = ttk.Combobox(root, textvariable=loader_tmp, state="readonly")

        id_gen = uuid.uuid1()
        self.hexid = id_gen.hex

        # Script show textbox
        self.lb2 = Label(self.root, text="File text")
        self.lb2.grid(row=4, column=1)
        self.text1 = Text(root, height=40, width=75)
        self.text1.grid(row=5, column=0, rowspan=3, columnspan=5)

        # root textbox
        self.lb3 = Label(self.root, text="Input text")
        self.lb3.grid(row=4, column=7)
        self.text3 = Text(root, height=40, width=75)
        self.text3.grid(row=5, column=5, rowspan=3, columnspan=5)

        # menu definition
        main_menu = Menu(root)

        self.menuSoubor = Menu(main_menu, tearoff=0)
        self.menuSoubor.add_command(label="Open", command=self.open_dialog_window)
        # lambda allows send argument without executing the command in init phase
        self.menuSoubor.add_separator()
        self.menuSoubor.add_command(label="Exit", command=root.quit)
        main_menu.add_cascade(label="File", menu=self.menuSoubor)

        seq_holder = IntVar()
        self.seq = Label(self.root, text="Sequence")
        self.textfield_seq = ttk.Entry(self.root, textvariable=seq_holder)

        db_deliver_holder = StringVar()
        self.db_deliver = Label(self.root, text="To database")
        self.textfield_db_deliver = ttk.Entry(self.root, textvariable=db_deliver_holder)

        root.config(menu=main_menu)

    def loader(self, list_files):
        self.cb1['values'] = list_files
        return

    # read filename, enable/disable buttons and other features
    def open_dialog_window(self):
        self.root.filename_open = filedialog.askdirectory()
        list_files = list()
        for file in Path(self.root.filename_open).iterdir():
            if file.suffix == ".txt":
                list_files.append(file.name)
        self.loader(list_files)
        btn = ttk.Button(self.root, text="To Stack", command=self.set_dict)
        btn.grid(row=1, column=4)
        btn2 = ttk.Button(self.root, text="Prepare DB", command=self.get_as_json)
        btn2.grid(row=1, column=7)
        btn3 = ttk.Button(self.root, text="Deploy", command=self.deploy_to_db)
        btn3.grid(row=1, column=8)
        self.l1.grid(row=0, column=2)
        self.cb1.grid(row=0, column=3)
        self.seq.grid(row=1, column=2)
        self.textfield_seq.grid(row=1, column=3)
        self.db_deliver.grid(row=0, column=4)
        self.textfield_db_deliver.grid(row=0, column=5)
        self.cb1.bind("<<ComboboxSelected>>", self.scripts_parser)

    def scripts_parser(self, event=None):
        logger.info(self.cb1.get())
        self.text1.config(state="normal")
        self.text1.delete("1.0", END)
        with open(Path(self.root.filename_open, self.cb1.get()), encoding="utf-8") as f:
            data = f.read()
            scripts = data.split(";")
            for script in scripts:
                self.text1.insert(END, script.strip() + "\n")
        self.text1.config(state="disabled")
        return scripts

    def set_dict_file(self):
        file = self.cb1.get()
        print(file)
        file_dict = dict()
        file_dict["filename"] = file
        file_dict["type"] = ".txt"
        file_dict["collection"] = 1
        file_dict["sequence"] = self.textfield_seq.get()
        list_of_user_input = str(self.text3.get("1.0", END)).strip().split(";")
        file_dict["user_query"] = list_of_user_input
        return file_dict

    @staticmethod
    def set_dict_metadata():
        metadata_dict = dict()
        metadata_dict["@app"] = "kb_hack"
        metadata_dict["@timestamp"] = time.time()
        return metadata_dict

    def set_dict(self):
        logger.info("Button To Stack was pressed!")
        self.full_dict["uid"] = self.hexid
        self.full_dict["username"] = self.textfield_login.get()
        self.full_dict["password"] = self.textfield_pass.get()
        self.full_dict["path"] = self.root.filename_open
        self.full_dict["database"] = self.textfield_db_deliver.get()
        self.full_dict["files"].append(self.set_dict_file())
        self.full_dict["metadata"] = self.set_dict_metadata()
        print(self.full_dict)
        return self.full_dict

    def get_as_json(self):
        logger.info("Prepare DB was pressed!")
        #self.start_monitor()
        print(json.dumps(self.full_dict))
        self.deploy_clean, self.deploy_dir = kokos(self.full_dict)
        return

    def deploy_to_db(self):
        logger.info("Button Deploy was pressed!")
        for file in Path(self.deploy_clean).iterdir():
            print(self.deploy_clean)
            print(self.deploy_dir)
            bteq_params("trfddl_wsp_hackaton_team3", "Team3Hackaton-BIGDataTeam", self.deploy_clean, file)
        for file in Path(self.deploy_dir).iterdir():
            bteq_params("trfddl_wsp_hackaton_team3", "Team3Hackaton-BIGDataTeam", self.deploy_dir, file)

    def config_init(self, filename='hack.yml') -> dict:
        try:
            cfg = yaml.safe_load(open(filename))
        except IOError:
            msg = f'Loading config file ({filename}) failed.'
            raise IOError(msg)
        return cfg

    def send_message(self, producer_conf: dict, metrics: str):
        logger.info(f"SEND MESSAGE: {metrics}")
        try:

            topic_name = "monitoring-app-in"
            producer = KafkaProducer(**producer_conf)
            value_bytes = bytes(str(metrics), encoding='utf-8')
            sender = producer.send(topic_name, value=value_bytes)
            record_metadata = sender.get(timeout=100)
            sender = producer.flush()
            logger.info(record_metadata)

        except Exception as excp:
            logger.info(f"Unexpected error: {excp}")
        else:
            producer.close()

    def generate_conf(self, cfg):

        producer_conf = {
            'bootstrap_servers': cfg["kafka"]["bootstrap_servers"],
            'client_id': cfg["kafka"]["producer_conf"]["client_id"],
            "api_version": (0,10,1),
            "security_protocol": cfg["kafka"]["security_protocol"],
            "sasl_mechanism": cfg["kafka"]["sasl_mechanism"],
            "ssl_check_hostname": bool(cfg["kafka"]["ssl_check_hostname"]),
            'ssl_keyfile': cfg["kafka"]["ssl_keyfile"],
            'ssl_certfile': cfg["kafka"]["ssl_certfile"],
            'ssl_password': cfg["kafka"]["ssl_password"],
            'ssl_cafile': cfg["kafka"]["ssl_cafile"],
            'acks': cfg["kafka"]["producer_conf"]["acks"]
        }
        return producer_conf

    def process_metrics(self, producer_conf,metrics):
        try:
            timestamp_ns = round(time.time() * (10 ** 9))
            metrics=f"{metrics} {timestamp_ns}"
            logger.info(metrics)
            starttime = datetime.now()
            self.send_message(producer_conf, metrics)
            endtime = datetime.now()
        except Exception:
            print_exc()
        else:
            timer = (endtime - starttime).total_seconds()
            print(f"Total time: {timer}")

        #TODO: METRICS SOURCE
    def start_monitor(self):
        cfg = self.config_init()
        producer_conf = self.generate_conf(cfg)
        noww=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        uid = '"' + self.hexid + '"'
        user = '"' + self.textfield_login.get() + '"'
        db = '"' + self.textfield_db_deliver.get() + '"'
        metrics = 'hack_monitoring,status=running hexid={},user={},db={}'.format(uid, user, db)
        self.process_metrics(producer_conf,metrics)
        print(f'Metrics values are: {metrics}')

window = Tk()
Window(window)
window.mainloop()

sys.exit()
