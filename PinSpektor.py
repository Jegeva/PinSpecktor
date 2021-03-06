#! /usr/bin/python3

# -*- coding: utf-8 -*-

# MIT license
#
# Copyright (C) 2021 @Jegeva.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pcbnew import *
import wx
import wx.aui
import wx.lib.filebrowsebutton as FBB
import os
import re

WIDGET_SPACING = 5

def debug_dialog(msg, exception=None):
    if exception:
        msg = "\n".join((msg, str(exception), traceback.format.exc()))
    dlg = wx.MessageDialog(None, msg, "", wx.OK)
    dlg.ShowModal()
    dlg.Destroy()

# totally ripped from WireIt

class LabelledTextCtrl(wx.BoxSizer):
    """Text-entry box with a label."""

    def __init__(self, parent, label, value, tooltip=""):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.lbl = wx.StaticText(parent=parent, label=label)
        self.ctrl = wx.TextCtrl(parent=parent, value=value, style=wx.TE_PROCESS_ENTER)
        self.ctrl.SetToolTip(wx.ToolTip(tooltip))
        self.AddSpacer(WIDGET_SPACING)
        self.Add(self.lbl, 0, wx.ALL | wx.ALIGN_CENTER)
        self.AddSpacer(WIDGET_SPACING)
        self.Add(self.ctrl, 1, wx.ALL | wx.EXPAND)
        self.AddSpacer(WIDGET_SPACING)

class LabelledListBox(wx.BoxSizer):
    """ListBox with label."""

    def __init__(self, parent, label, choices, tooltip="",size=(0,0),horiz=0):
        if horiz:
            wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        else:
            wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.lbl = wx.StaticText(parent=parent, label=label)
        self.lbx = wx.ListBox(
            parent=parent,
            choices=choices,
            style=wx.LB_MULTIPLE | wx.LB_NEEDED_SB | wx.LB_SORT,
            size=size
        )
        self.lbx.SetToolTip(wx.ToolTip(tooltip))
        self.AddSpacer(WIDGET_SPACING)
        self.Add(self.lbl, 0, wx.ALL | wx.ALIGN_TOP)
        self.AddSpacer(WIDGET_SPACING)
        self.Add(self.lbx, 1, wx.ALL | wx.EXPAND)
        self.AddSpacer(WIDGET_SPACING)

class LabelledComboBox(wx.BoxSizer):
    """ListBox with label."""

    def __init__(self, parent, label, choices, tooltip=""):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.lbl = wx.StaticText(parent=parent, label=label)
        self.cbx = wx.ComboBox(
            parent=parent,
            choices=choices,
            style=wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER | wx.CB_SORT,
        )
        self.cbx.SetToolTip(wx.ToolTip(tooltip))
        self.AddSpacer(WIDGET_SPACING)
        self.Add(self.lbl, 0, wx.ALL | wx.ALIGN_TOP)
        self.AddSpacer(WIDGET_SPACING)
        self.Add(self.cbx, 1, wx.ALL | wx.EXPAND)
        self.AddSpacer(WIDGET_SPACING)


class LabelledCheckBox(wx.BoxSizer):
    def __init__(self, parent, label, tooltip=""):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.ckbx = wx.CheckBox(
            parent=parent,
            label = label,
            style=wx.CHK_3STATE
        )
        self.AddSpacer(WIDGET_SPACING)
        self.Add(self.ckbx, 0, wx.ALL | wx.ALIGN_TOP)

class Labelled2CheckBox(wx.BoxSizer):
    def __init__(self, parent, label, tooltip=""):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.ckbx = wx.CheckBox(
            parent=parent,
            label = label,
            style=wx.CHK_3STATE
        )
        self.AddSpacer(WIDGET_SPACING)
        self.Add(self.ckbx, 0, wx.ALL | wx.ALIGN_TOP)

class PageF(wx.Panel):
    pc=None
    smc=None
    spac=None
    spr=None
    dr=None
    dv=None
    psd=None
    def __init__(self, parent,psd):
        wx.Panel.__init__(self, parent)
        self.psd=psd
        self.s= wx.BoxSizer(wx.VERTICAL)
        self.dr       = LabelledCheckBox(self, "Display ref", "")
        self.dv       = LabelledCheckBox(self, "Display val", "")
        self.pc  =LabelledTextCtrl(self, "Pad clearance (mm)"            ,"" , "")
        self.smc =LabelledTextCtrl(self, "Solder mask clearance (mm)"    ,"" , "")
        self.spac=LabelledTextCtrl(self, "Solder paste abs clearance (mm)","" , "")
        self.spr =LabelledTextCtrl(self, "Solder paste retraction (%)"   ,"" , "")
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.dr, 0, wx.ALL |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.dv, 0, wx.ALL |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.pc, 0, wx.ALL |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.smc, 0, wx.ALL |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.spac, 0, wx.ALL  |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.spr, 0, wx.ALL  |  wx.EXPAND)
        self.SetSizer(self.s)
        self.Layout()
        self.Fit()

    def getdr(self):
        return(self.dr)
    def getdv(self):
        return(self.dv)

    def getallsilk(self):
        return(self.allsilk)

    def getpc(self):
        return(self.pc)

    def getsmc(self):
        return(self.smc)

    def getspac(self):
        return(self.spac)

    def getspr(self):
        return(self.spr)


class PageP(wx.Panel):
    pc=None
    smc=None
    spac=None
    spr=None
    psd=None
    def __init__(self, parent,psd):
        wx.Panel.__init__(self, parent)
        self.psd=psd
        self.s= wx.BoxSizer(wx.VERTICAL)
        self.pc  =LabelledTextCtrl(self, "Pad clearance (mm)"            ,"" , "")
        self.smc =LabelledTextCtrl(self, "Solder mask clearance (mm)"    ,"" , "")
        self.spac=LabelledTextCtrl(self, "Solder paste abs clearance (mm)","" , "")
        self.spr =LabelledTextCtrl(self, "Solder paste retraction (%)"   ,"" , "")
        self.s.Add(self.pc, 0, wx.ALL |  wx.EXPAND| wx.ALIGN_TOP)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.smc, 0, wx.ALL |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.spac, 0, wx.ALL  |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.spr, 0, wx.ALL  |  wx.EXPAND)
        self.SetSizer(self.s)
        self.Layout()
        self.Fit()

    def getpc(self):
        return(self.pc)

    def getsmc(self):
        return(self.smc)

    def getspac(self):
        return(self.spac)

    def getspr(self):
        return(self.spr)


def getCopperActiveLayers():
    b=GetBoard()
    return [
        b.GetLayerName(lid)
        for lid in range(PCBNEW_LAYER_ID_START,PCB_LAYER_ID_COUNT)
        if b.GetEnabledLayers().Contains(lid) and IsCopperLayer(lid)
    ]

class PageN(wx.Panel):
    useclass  =None
    clearance =None
    trackw    =None
    viasz     =None
    viahole   =None
    uviasz    =None
    uviahole  =None
    dpwidth   =None
    dpgap     =None

    onlyonlayer = None
    selectedlayer = None
    psd = None
    def __init__(self, parent,psd):
        wx.Panel.__init__(self, parent)
        self.psd=psd
        self.s= wx.BoxSizer(wx.VERTICAL)
        self.useclass  =LabelledCheckBox(self, "Use net class values", "")
        self.trackw    =LabelledTextCtrl(self, "Track width"            ,"" , "")
        self.viasz     =LabelledTextCtrl(self, "Via Size"            ,"" , "")
        self.viahole   =LabelledTextCtrl(self, "Via Hole"            ,"" , "")
        self.uviasz    =LabelledTextCtrl(self, "??Via Size"            ,"" , "")
        self.uviahole  =LabelledTextCtrl(self, "??Via Hole"            ,"" , "")
        self.onlyonlayer = Labelled2CheckBox(self, "Only apply to these layers", "")
        self.selectionlb = wx.ListBox(
            parent=self,
            choices= getCopperActiveLayers()
            ,
            style=wx.LB_MULTIPLE | wx.LB_NEEDED_SB | wx.LB_SORT,
        )
        self.selectionlb.Enable(False)


        self.s.Add(self.useclass, 0, wx.ALL |  wx.EXPAND| wx.ALIGN_TOP)
        self.s.AddSpacer(WIDGET_SPACING)

        self.s.Add(self.clearance, 0, wx.ALL |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)

        self.s.Add(self.trackw, 0, wx.ALL  |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)

        self.s.Add(self.viasz, 0, wx.ALL  |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.viahole, 0, wx.ALL  |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.uviasz, 0, wx.ALL  |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.uviahole, 0, wx.ALL  |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)

        self.s.Add(self.onlyonlayer, 0, wx.ALL  |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.selectionlb, 0, wx.ALL  |  wx.EXPAND)


        self.SetSizer(self.s)
        self.Layout()
        self.Fit()

        self.onlyonlayer.ckbx.Bind(wx.EVT_CHECKBOX,self.clickOnlyOnLayer,self.onlyonlayer.ckbx)
        self.useclass.ckbx.Bind(wx.EVT_CHECKBOX,self.clickUseClass,self.useclass.ckbx)

    def clickOnlyOnLayer(self,evt):
        if(self.selectionlb.IsEnabled()):
            self.selectionlb.Enable(False)
        else:
            self.selectionlb.Enable(True)

    def clickUseClass(self,evt):
        if(self.trackw.ctrl.IsEnabled()):
            self.trackw.ctrl.SetValue("")
            self.trackw.ctrl.Enable(False)
            self.viasz.ctrl.SetValue("")
            self.viasz.ctrl.Enable(False)
            self.uviasz.ctrl.SetValue("")
            self.uviasz.ctrl.Enable(False)
            self.viahole.ctrl.SetValue("")
            self.viahole.ctrl.Enable(False)
            self.uviahole.ctrl.SetValue("")
            self.uviahole.ctrl.Enable(False)
            self.onlyonlayer.ckbx.Enable(False)
            self.selectionlb.Enable(False)
        else:
            self.trackw.ctrl.Enable(True)
            self.viahole.ctrl.Enable(True)
            self.uviahole.ctrl.Enable(True)
            self.viasz.ctrl.Enable(True)
            self.uviasz.ctrl.Enable(True)
            self.onlyonlayer.ckbx.Enable(True)

            if(self.onlyonlayer.ckbx.GetValue()):
                self.selectionlb.Enable(True)

            #print(self.psd.selectionlb.lbx.GetSelections())
            self.psd.lbsclicked(None)


        return

    def getUseClass(self):
        return self.useclass
    def getTrackW(self):
        return self.trackw
    def getViaSz(self):
        return self.viasz
    def getViaHole(self):
        return self.viahole
    def getUViaSz(self):
        return self.uviasz
    def getUViahole(self):
        return self.uviahole
    def getOnlyLayer(self):
        return self.onlyonlayer
    def getSelLayer(self):
        return self.selectionlb






#def getPcbnewItemByClassAndREName(itype,rename):
#    typeclassh = {
#        "f":FOOTPRINT,
#        "n":NETINFO_ITEM,
#        "p":PAD
#    }
#    iclass = typeclassh[itype]

class PinSpektorDialog(wx.Dialog):
    searchre = '.'
    searchtype = 'f'
    brd = None
    currSearch_results=None;
    currSelection=None;
    def __init__(self, *args, **kwargs):
        try:

            wx.Dialog.__init__(self, None, title=kwargs.get("title"))
            panel = wx.Panel(self)
            self.brd=kwargs.get("brd")

            self.searchre_field = LabelledTextCtrl(
                panel, "Search:", self.searchre , "search fields (regexp)")
            self.searchre_field.ctrl.Bind(
                wx.EVT_TEXT, self.set_searchre, self.searchre_field.ctrl
            )

            self.selectionlb = LabelledListBox( panel, "Choices", [] , "",size=(100, 600) )

            self.selectionlb.lbx.Bind(wx.EVT_LISTBOX,self.lbsclicked,self.selectionlb.lbx)

            self.ok_btn = wx.Button(panel, label="Apply")
            self.cancel_btn = wx.Button(panel, label="Cancel")
            self.ok_btn.Bind(wx.EVT_BUTTON, self.applyfun, self.ok_btn)
            self.cancel_btn.Bind(wx.EVT_BUTTON, self.cancel, self.cancel_btn)

            btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
            btn_sizer.AddSpacer(WIDGET_SPACING)
            btn_sizer.Add(self.ok_btn, flag=wx.ALL | wx.ALIGN_CENTER)
            btn_sizer.AddSpacer(WIDGET_SPACING)
            btn_sizer.Add(self.cancel_btn, flag=wx.ALL | wx.ALIGN_CENTER)
            btn_sizer.AddSpacer(WIDGET_SPACING)

            main_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.left_sizer = wx.BoxSizer(wx.VERTICAL,)
            self.left_sizer.Add(self.searchre_field, 0, wx.ALL | wx.EXPAND, WIDGET_SPACING)

            self.nb = wx.Notebook(panel,size=(400, 600))
            self.pages = [ PageF(self.nb,self), PageN(self.nb,self), PageP(self.nb,self)]

            self.nb.AddPage(self.pages[0], "Footprint")
            self.nb.AddPage(self.pages[1], "Net")
            self.nb.AddPage(self.pages[2], "Pin")
            self.currpage=self.pages[0]

            self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,self.pagechanged,self.nb)

            self.left_sizer.Add(self.nb,1, wx.ALL | wx.EXPAND, WIDGET_SPACING);
            right_sizer = wx.BoxSizer(wx.VERTICAL)
            right_sizer.Add(self.selectionlb, 0, wx.ALL | wx.EXPAND, WIDGET_SPACING)

            main_sizer.Add(self.left_sizer , 0, wx.ALL , WIDGET_SPACING)
            main_sizer.Add(right_sizer, 0, wx.ALL , WIDGET_SPACING)

            # Create a vertical sizer to hold everything in the panel.
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(main_sizer, 0, wx.ALL | wx.EXPAND, WIDGET_SPACING)
            sizer.Add(btn_sizer , 0, wx.ALL | wx.ALIGN_CENTER, WIDGET_SPACING)
            # Size the panel.
            panel.SetSizer(sizer)
            panel.Layout()
            panel.Fit()
            # Finally, size the frame that holds the panel.

            self.update_search()
            self.Fit()

            # Show the dialog box.
            self.ShowModal()

        except Exception as e:
            debug_dialog("Something went wrong!", e)


    def pagechanged(self,evt):
        sel = evt.GetSelection()
        self.currpage=self.pages[sel]
        if(isinstance(self.pages[sel],PageP)):
            self.searchtype = 'p'
        if(isinstance(self.pages[sel],PageN)):
            self.searchtype = 'n'
        if(isinstance(self.pages[sel],PageF)):
            self.searchtype = 'f'
        self.update_search()
        return


    def lbsclicked_f(self,selected):
        v_pclear    = None
        v_smclear   = None
        v_spabsclear= None
        v_spretractr= None
        v_dr= None
        v_dv= None
        v_oslkti= None

        page=self.currpage
        rs=""
        self.currSelection=[]
        print()
        for s in selected:
            #debug_dialog("lbsc 0 "+str(s))
            #f=self.currSearch_results[s]["f"]
            p=self.currSearch_results[s]["f"]
            self.currSearch_results[s]["sel"]=True
            self.currSelection.append(s)

            if(v_pclear == None):
                v_pclear       =p.GetLocalClearance()/1e6
                v_smclear      =p.GetLocalSolderMaskMargin()/1e6
                v_spretractr   =p.GetLocalSolderPasteMarginRatio()*100
                v_dr           =p.Reference().IsVisible()
                v_dv           =p.Value().IsVisible()
                tmp            =p.GetLocalSolderPasteMargin()
                if(isinstance(tmp,wxSize)):
                    v_spabsclear   =((tmp[0]+tmp[1])/2)/1e6
                else:
                    v_spabsclear   =tmp/1e6
            else:
                tv_pclear      =p.GetLocalClearance()/1e6
                tv_smclear     =p.GetLocalSolderMaskMargin()/1e6
                tv_spretractr  =p.GetLocalSolderPasteMarginRatio()*100
                tv_dr           =p.Reference().IsVisible()
                tv_dv           =p.Value().IsVisible()

                tmp            =p.GetLocalSolderPasteMargin()
                if(isinstance(tmp,wxSize)):
                    tv_spabsclear   =((tmp[0]+tmp[1])/2)/1e6
                else:
                    tv_spabsclear   =tmp/1e6

                if(tv_pclear != v_pclear):
                    v_pclear="MULTIPLE VALUES"
                if(tv_smclear != v_smclear):
                    v_smclear="MULTIPLE VALUES"
                if(tv_spabsclear != v_spabsclear):
                    v_spabsclear="MULTIPLE VALUES"
                if(tv_spretractr != v_spretractr):
                    v_spretractr="MULTIPLE VALUES"
                if(v_dr != tv_dr):
                    v_dr = wx.CHK_UNDETERMINED
                if(v_dv != tv_dv):
                    v_dv = wx.CHK_UNDETERMINED
        page.getpc().ctrl.SetValue(str(v_pclear))
        page.getsmc().ctrl.SetValue(str(v_smclear))
        page.getspac().ctrl.SetValue(str(v_spabsclear))
        page.getspr().ctrl.SetValue(str(v_spretractr))
        if(v_dr == False):
            page.getdr().ckbx.Set3StateValue(wx.CHK_UNCHECKED)
        else:
            if(v_dr == wx.CHK_UNDETERMINED):
                page.getdr().ckbx.Set3StateValue(wx.CHK_UNDETERMINED)
            else:
                page.getdr().ckbx.Set3StateValue(wx.CHK_CHECKED)
        if(v_dv == False):
            page.getdv().ckbx.Set3StateValue(wx.CHK_UNCHECKED)
        else:
            if(v_dv == wx.CHK_UNDETERMINED):
                page.getdv().ckbx.Set3StateValue(wx.CHK_UNDETERMINED)
            else:
                page.getdv().ckbx.Set3StateValue(wx.CHK_CHECKED)

    def lbsclicked_p(self,selected):
        v_pclear    = None
        v_smclear   = None
        v_spabsclear= None
        v_spretractr= None
        page=self.currpage
        rs=""
        self.currSelection=[]

        for s in selected:
            #debug_dialog("lbsc 0 "+str(s))
            #f=self.currSearch_results[s]["f"]
            p=self.currSearch_results[s]["p"]
            self.currSearch_results[s]["sel"]=True
            self.currSelection.append(s)

            if(v_pclear == None):
                v_pclear       =p.GetLocalClearance()/1e6
                v_smclear      =p.GetLocalSolderMaskMargin()/1e6
                v_spretractr   =p.GetLocalSolderPasteMarginRatio()*100
                tmp            =p.GetLocalSolderPasteMargin()
                if(isinstance(tmp,wxSize)):
                    v_spabsclear   =((tmp[0]+tmp[1])/2)/1e6
                else:
                    v_spabsclear   =tmp/1e6
            else:
                tv_pclear      =p.GetLocalClearance()/1e6
                tv_smclear     =p.GetLocalSolderMaskMargin()/1e6
                tv_spretractr  =p.GetLocalSolderPasteMarginRatio()*100
                tmp            =p.GetLocalSolderPasteMargin()
                if(isinstance(tmp,wxSize)):
                    tv_spabsclear   =((tmp[0]+tmp[1])/2)/1e6
                else:
                    tv_spabsclear   =tmp/1e6
                if(tv_pclear != v_pclear):
                    v_pclear="MULTIPLE VALUES"
                if(tv_smclear != v_smclear):
                    v_smclear="MULTIPLE VALUES"
                if(tv_spabsclear != v_spabsclear):
                    v_spabsclear="MULTIPLE VALUES"
                if(tv_spretractr != v_spretractr):
                    v_spretractr="MULTIPLE VALUES"
        page.getpc().ctrl.SetValue(str(v_pclear))
        page.getsmc().ctrl.SetValue(str(v_smclear))
        page.getspac().ctrl.SetValue(str(v_spabsclear))
        page.getspr().ctrl.SetValue(str(v_spretractr))

        return


    def lbsclicked_n(self,selected):

        v_useclass  = False
        v_trackw    =None
        v_viasz     =None
        v_viahole   =None
        v_uviasz    =None
        v_uviahole  =None
        page=self.currpage
        self.currSelection=[]
        for s in selected:
            self.currSelection.append(s)

            n=self.currSearch_results[s]["n"]
            self.currSearch_results[s]["sel"]=True

            for t in self.currSearch_results[s]["tracks"]:
                if(v_trackw == None):
                    v_trackw    = t.GetWidth()/1e6
                else:
                    if( v_trackw!= t.GetWidth()/1e6):
                        v_trackw = "MULTIPLE VALUES"

            for t in self.currSearch_results[s]["vias"]:
                #print("via type",t.GetViaType())
                if(t.GetViaType() == VIATYPE_MICROVIA):
                    if(v_uviasz == None):
                        v_uviasz    = t.GetWidth()/1e6
                        v_uviahole  = t.GetDrill()/1e6

                    else:
                        if( v_uviasz!= t.GetWidth()/1e6):
                            v_uviasz = "MULTIPLE VALUES"
                        if( v_uviahole!= t.GetDrill()/1e6):
                            v_uviahole = "MULTIPLE VALUES"

                if(t.GetViaType() == VIATYPE_THROUGH):
                    if(v_viasz == None):
                        v_viasz    = t.GetWidth()/1e6
                        v_viahole  = t.GetDrill()/1e6

                    else:
                        if( v_viasz!= t.GetWidth()/1e6):
                            v_viasz = "MULTIPLE VALUES"
                        if( v_viahole!= t.GetDrill()/1e6):
                            v_viahole = "MULTIPLE VALUES"

        if(v_trackw):
            page.getTrackW().ctrl.SetValue(str(v_trackw))
        if(v_viasz):
            page.getViaSz().ctrl.SetValue(str(v_viasz))
        if(v_viahole):
            page.getViaHole().ctrl.SetValue(str(v_viahole))
        if(v_uviasz):
            page.getUViaSz().ctrl.SetValue(str(v_uviasz))
        if(v_uviahole):
            page.getUViaHole().ctrl.SetValue(str(v_uviahole))

        return



    def lbsclicked(self,evt):
        selected =  [self.selectionlb.lbx.GetString(i) for i in self.selectionlb.lbx.GetSelections()]
        #debug_dialog("seleected "+str(selected))
        if( self.searchtype == 'f'):
            self.lbsclicked_f(selected)
        if( self.searchtype == 'p'):
            self.lbsclicked_p(selected)
        if( self.searchtype == 'n'):
            self.lbsclicked_n(selected)

    def update_search(self):
        try:
            #
            cre = re.compile(self.searchre_field.ctrl.GetValue())
        except Exception as e:
            self.searchre_field.ctrl.SetForegroundColour(wx.Colour(255,0,0))
            return
        self.searchre_field.ctrl.SetForegroundColour(wx.Colour(0,0,0))
        self.selectionlb.lbx.Clear()
        self.currSearch_results={}
        if( self.searchtype == 'f'):
            for f in self.brd.GetFootprints():
                if(cre.search(f.GetReference())):
                    self.currSearch_results[f.GetReference()]={}
                    self.currSearch_results[f.GetReference()]["f"]=f

        if( self.searchtype == 'p'):
            #debug_dialog("*")
            fs= self.brd.GetFootprints()

            for f in fs:
                for p in f.Pads():
                    s =f.GetReference()+"/"+p.GetName()
                    if(cre.search(s)):
                        self.currSearch_results[s] = {}
                        self.currSearch_results[s]["f"]=f
                        self.currSearch_results[s]["p"]=p

        if( self.searchtype == 'n'):
            #debug_dialog("*")
            nbn = self.brd.GetNetsByName()
            for n in nbn.keys():
                sn= str(n)
                #print(sn)
                if(len(sn)):
                    if(cre.search(sn)):
                        if(sn[:4]!="no_c"):
                            self.currSearch_results[sn] = {}
                            self.currSearch_results[sn]["n"] = nbn[n]
                            self.currSearch_results[sn]["tracks"] =[t for t in self.brd.GetTracks() if ((str(t.GetNet().GetNetname())==sn) and
                                                                                                    (
                                                                                                        isinstance(t,TRACK) and not
                                                                                                        isinstance(t,VIA)
                                                                                                    ))]
                            self.currSearch_results[sn]["vias"]   =[t for t in self.brd.GetTracks() if ((str(t.GetNet().GetNetname())==sn) and isinstance(t,VIA  ))]



        lst= list(self.currSearch_results.keys())
        self.selectionlb.lbx.InsertItems(lst,0)
        return

    def apply_p(self):
        page=self.currpage
        tpc  =page.getpc().ctrl.GetValue()
        tsmc =page.getsmc().ctrl.GetValue()
        tspac=page.getspac().ctrl.GetValue()
        tspr =page.getspr().ctrl.GetValue()
        for sel in self.currSelection:
            p = self.currSearch_results[sel]["p"]
            try:
                pc=float(tpc)
                p.SetLocalClearance(int(pc*1e6))
            except ValueError as e:
                pass
            try:
                smc=float(tsmc)
                p.SetLocalSolderMaskMargin(int(smc*1e6))
            except ValueError as e:
                pass
            try:
                spac=float(tspac)
                p.SetLocalSolderPasteMargin(int(spac*1e6))
            except ValueError as e:
                pass
            try:
                spr=float(tspr)
                p.SetLocalSolderPasteMarginRatio(spr/100.0)
            except ValueError as e:
                pass
        return

    def apply_f(self):
        page=self.currpage
        tpc  =page.getpc().ctrl.GetValue()
        tsmc =page.getsmc().ctrl.GetValue()
        tspac=page.getspac().ctrl.GetValue()
        tspr =page.getspr().ctrl.GetValue()
        tdr  =page.getdr().ckbx.Get3StateValue()
        tdv  =page.getdv().ckbx.Get3StateValue()
        for sel in self.currSelection:
            p = self.currSearch_results[sel]["f"]
            try:
                pc=float(tpc)
                p.SetLocalClearance(int(pc*1e6))
            except ValueError as e:
                pass
            try:
                smc=float(tsmc)
                p.SetLocalSolderMaskMargin(int(smc*1e6))
            except ValueError as e:
                pass
            try:
                spac=float(tspac)
                p.SetLocalSolderPasteMargin(int(spac*1e6))
            except ValueError as e:
                pass
            try:
                spr=float(tspr)
                p.SetLocalSolderPasteMarginRatio(spr/100.0)
            except ValueError as e:
                pass
            if(tdr!=wx.CHK_UNDETERMINED):
                if(tdr==wx.CHK_CHECKED):
                    p.Reference().SetVisible(True)
                else:
                    p.Reference().SetVisible(False)
            if(tdv!=wx.CHK_UNDETERMINED):
                if(tdv==wx.CHK_CHECKED):
                    p.Value().SetVisible(True)
                else:
                    p.Value().SetVisible(False)

        return


    def apply_n(self):
        page=self.currpage

        v_useclass  =None
        v_trackw    =None
        v_viasz     =None
        v_viahole   =None
        v_uviasz    =None
        v_uviahole  =None
        v_onlylayer =None
        v_tlayers   =None

        v_useclass  = page.getUseClass().ckbx.GetValue()

        try:
            v_trackw    = float(page.getTrackW().ctrl.GetValue())
        except ValueError as e:
            pass
        try:
            v_viasz     = float(page.getViaSz().ctrl.GetValue())
        except ValueError as e:
            pass
        try:
            v_viahole   = float(page.getViaHole().ctrl.GetValue())
        except ValueError as e:
            pass
        try:
            v_uviasz    = float(page.getUViaSz().ctrl.GetValue())
        except ValueError as e:
            pass
        try:
            v_uviahole  = float(page.getUViahole().ctrl.GetValue())
        except ValueError as e:
            pass

        v_onlylayer = page.getOnlyLayer().ckbx.GetValue()
        v_tlayers   = [ page.getSelLayer().GetString(i) for i in page.getSelLayer().GetSelections()]

        print(v_tlayers)

        for s in self.currSelection :
            if(v_useclass):
                netclasses=self.brd.GetDesignSettings().GetNetClasses()
                defaultClass = netclasses.GetDefault()
                d_trackw=defaultClass.GetTrackWidth()
                d_viasz=defaultClass.GetViaDiameter()
                d_viahole=defaultClass.GetViaDrill()
                d_uviasz=defaultClass.GetuViaDiameter()
                d_uviahole=defaultClass.GetuViaDrill()

                if(self.brd.GetDesignSettings().GetNetClasses().GetCount() == 0):
                    v_trackw    = d_trackw
                    v_viasz     = d_viasz
                    v_viahole   = d_viahole
                    v_uviasz    = d_uviasz
                    v_uviahole  = d_uviahole

            for t in self.currSearch_results[s]["tracks"]:

                if(v_onlylayer and (self.brd.GetLayerName(t.GetLayer()) not in v_tlayers)):
                    continue

                if(v_useclass):
                    if(t.GetNetClassName() == "Default"):
                        t.SetWidth(defaultClass.GetTrackWidth())
                    else :
                        t.SetWidth(netclasses.NetClasses()[t.GetNetClassName()].GetTrackWidth())
                else:
                    if(v_trackw):
                        t.SetWidth(int(v_trackw*1e6))

            for t in self.currSearch_results[s]["vias"]:
                if(t.GetViaType() == VIATYPE_MICROVIA):
                    if(v_useclass):
                        if(t.GetNetClassName() == "Default"):
                            t.SetDrill(defaultClass.GetuViaDrill())
                            t.SetWidth(defaultClass.GetuViaDiameter())

                        else :
                            t.SetDrill(netclasses.NetClasses()[t.GetNetClassName()].GetuViaDrill())
                            t.SetWidth(netclasses.NetClasses()[t.GetNetClassName()].GetuViaDiameter())

                    else:
                        if(v_uviasz != None):
                            t.SetWidth(int(v_uviasz*1e6))
                            t.SetDrill(int(v_uviahole*1e6))
                if(t.GetViaType() == VIATYPE_THROUGH):
                    if(v_useclass):
                        if(t.GetNetClassName() == "Default"):
                            t.SetDrill(defaultClass.GetViaDrill())
                            t.SetWidth(defaultClass.GetViaDiameter())

                        else :
                            t.SetDrill(netclasses.NetClasses()[t.GetNetClassName()].GetViaDrill())
                            t.SetWidth(netclasses.NetClasses()[t.GetNetClassName()].GetViaDiameter())

                    else:
                        if(v_viasz != None):
                            t.SetWidth(int(v_viasz*1e6))
                            t.SetDrill(int(v_viahole*1e6))

        return

    def applyfun(self, evt):
        if(self.searchtype == 'p'):
            self.apply_p()
        if(self.searchtype == 'f'):
            self.apply_f()
        if(self.searchtype == 'n'):
            self.apply_n()
        Refresh()
        return

    def set_searchre(self, evt):
        self.update_search()
        self.searchre = self.searchre_field.ctrl.GetValue()


    def cancel(self, evt):
        self.searchre = '.'
        #self.searchtype = FOOTPRINT
        #self.Show(False)
        #self.Close()
        self.EndModal(0)

def get_stuff_on_nets(*nets):
    """Get all the pads, tracks, zones attached to a net."""
    brd = GetBoard()
    all_stuff = list(brd.GetPads())
    all_stuff.extend(brd.GetTracks())
    all_stuff.extend(brd.Zones())
    stuff = []

    hum=FOOTPRINT

    for net in nets:
        if isinstance(net, int):
            stuff.extend([thing for thing in all_stuff if thing.GetNetCode() == net])
        elif isinstance(net, NETINFO_ITEM):
            stuff.extend([thing for thing in all_stuff if thing.GetNet() == net])
        else:
            stuff.extend([thing for thing in all_stuff if thing.GetNetname() == net])
    return stuff

def getbrd():
    return GetBoard()

class PinSpektorPlugin(ActionPlugin):
    pin_inspecter = None

    @staticmethod
    def getPSD(self):
        if(PinSpektorPlugin.pin_inspecter == None):
            PinSpektorPlugin.pin_inspecter=PinSpektorDialog(title="Inspect Pins",tool_tip="",brd=getbrd())
        PinSpektorPlugin.pin_inspecter.ShowModal()
        return PinSpektorPlugin.pin_inspecter


    def findPcbnewWindow(self):
        """Find the window for the PCBNEW application."""
        windows = wx.GetTopLevelWindows()
        pcbnew = [w for w in windows if (("Pcbnew" in w.GetTitle()) or ("PCB Editor") in  w.GetTitle())]
        if len(pcbnew) != 1:
            raise Exception("Cannot find pcbnew window from title matching!")
        return pcbnew[0]

    def defaults(self):
        self.name = "PinSpektor"
        self.category = "Inspect pins and nets"
        self.description = "looks and changes pin related stuff"
        self.brd = GetBoard()
        self.button_inited = False;

    def Run(self):

        if(not self.button_inited):
            #for i in range(20):
            #    print("\n")
            try:
                top_toolbar = wx.FindWindowById(ID_H_TOOLBAR, parent=self.findPcbnewWindow())

                path = os.path.dirname(os.path.realpath(__file__))

                PinSpektor_button = wx.NewId()
                PinSpektor_button_bm = wx.Bitmap(
                    os.path.join(path, "PinSpektor", "PinSpektor.png"),
                    wx.BITMAP_TYPE_PNG,
                )
                #debug_dialog(PinSpektor_button_bm)
                top_toolbar.AddTool(
                    PinSpektor_button,
                    "PinSpektor",
                    PinSpektor_button_bm,
                    "Inspect Pins",
                    wx.ITEM_NORMAL,
                )
                top_toolbar.Bind(wx.EVT_TOOL, PinSpektorPlugin.getPSD, id=PinSpektor_button)
            except Exception as e:
                debug_dialog("Something went wrong!", e)


            top_toolbar.Realize()
            self.button_inited = True  # Buttons now installed in toolbar.
            self.pin_inspecter = self.getPSD(self)

PinSpektorPlugin().register() # Instantiate and register to Pcbnew
