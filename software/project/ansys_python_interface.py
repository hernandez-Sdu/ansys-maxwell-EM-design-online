# python & ansoft connection

import os

import pythoncom
from win32com import client


def find_or_initial_project(ctx):
    print('Initial project: ' + ctx["data"]["project_folder"])
    print(ctx["params"]["spec_params"])

    # import ipdb; ipdb.set_trace()
    pythoncom.CoInitialize()
    oAnsoftApp = client.Dispatch("Ansoft.ElectronicsDesktop")

    oDesktop = oAnsoftApp.GetAppDesktop()
    oProject = oDesktop.NewProject()
    # project
    # if len(oDesktop.GetProjects()) == 0:
    #     oProject = oDesktop.NewProject()
    # else:
    #     oProject = oDesktop.GetActiveProject()

    oDesign = oProject.InsertDesign(
        "Maxwell 2D", "Maxwell2DDesign1", "Transient", "")
    # find previous project
    # if len(oProject.GetTopDesignList()) == 0:
    #     oDesign = oProject.InsertDesign("Maxwell 2D", "Maxwell2DDesign1", "Transient", "")
    # else:
    #     oDesign = oProject.GetActiveDesign()

    oEditor = oDesign.SetActiveEditor("3D Modeler")

    ctx["ansys_object"]["oProject"] = oProject
    ctx["ansys_object"]["oDesign"] = oDesign
    ctx["ansys_object"]["oEditor"] = oEditor
    ctx["ansys_object"]["oDesktop"] = oDesktop

    return ctx


def save_project(ctx):
    export_path = ctx["data"]["export_path"]
    project_name = ctx["data"]["project_name"]

    if not os.path.isdir(export_path):
        os.mkdir(export_path)

    ctx["ansys_object"]["oProject"].SaveAs(
        export_path + "\\" + project_name + ".aedt", True)

    return ctx


def close_project(ctx):
    project_name = ctx["data"]["project_name"]

    ctx["ansys_object"]["oDesktop"].CloseProject(project_name)

    return ctx
