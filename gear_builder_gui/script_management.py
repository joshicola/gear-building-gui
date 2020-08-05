import json
import os
import os.path as op

from PyQt5 import QtCore, QtGui, QtWidgets

# TODO: Very rudimentary at the moment. Would like to introduce
# elements to both create and interpret mustache tags (e.g. {{keyword}}) with the following
# intentions:
# tags: replace these with txt/keyword/config_value or nothing/comments
#       --this could be added to with a cbo_box that selects config key/value specifications
#       --call it 'config_vals:'?
# snippets: replace these with specified chunks of code or nothing/comments
# run_code: replace these with the output of code run on manifest or nothing/comments


class Script_Management:
    def __init__(self, main_window):
        self.ui = main_window.ui
        # Set the script template data
        self.ui.cbo_script_template.setItemData(0, ["script_library/simple_script/run.py"])
        self.ui.cbo_script_template.setItemData(
            1,
            [
                "script_library/build_validate_execute/run.py",
                "script_library/build_validate_execute/utils/args.py",
            ],
        )

    def save(self, directory):
        # is_simple_script = self.ui.ck_simple_script.isChecked()

        # if is_simple_script:
        #     script_str = open(
        #         op.join(source_dir, 'script_library/simple_script/run.py'),
        #         'r'
        #     ).read()
        #     script_str = script_str.replace('{name}', self.ui.txt_name.text())
        #     script_str = script_str.replace(
        #         '{base_command}',
        #         self.ui.txt_simple_script.text()
        #     )

        #     out_file = open(op.join(directory,'run.py'),'w')
        #     out_file.write(script_str)
        #     out_file.close()

        source_dir = op.join(os.path.dirname(os.path.realpath(__file__)), "..")
        cbo_script_data = self.ui.cbo_script_template.currentData()
        for fl in cbo_script_data:
            script_str = open(op.join(source_dir, fl)).read()
            script_str = script_str.replace("{{name}}", self.ui.txt_name.text())
            script_str = script_str.replace("{{base_command}}", self.ui.txt_simple_script.text())
            dirs = op.dirname(fl).split("/")
            basedir = op.join(dirs[0], dirs[1], "")
            if len(dirs) > 2:
                os.makedirs(op.join(directory, dirs[2]), exist_ok=True)

            open(op.join(directory, fl.replace(basedir, "")), "w").write(script_str)
