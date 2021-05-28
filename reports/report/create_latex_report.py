import os.path

from src.notebook_to_latex import convert_notebook_to_latex
import reports


notebook_path = os.path.join(reports.path,'report','01.1.report.ipynb')
build_directory = os.path.join(reports.path,'report_latex')

if not os.path.exists(build_directory):
    os.mkdir(build_directory)

skip_figures=False
convert_notebook_to_latex(notebook_path=notebook_path, build_directory=build_directory, save_main=False, skip_figures=skip_figures)