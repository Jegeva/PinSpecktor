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


class PageF(wx.Panel):
    pc=None
    smc=None
    spac=None
    spr=None
    dr=None
    dv=None
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
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
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
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

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.s= wx.BoxSizer(wx.VERTICAL)
        self.useclass  =LabelledCheckBox(self, "Use net class values", "")
        self.clearance =LabelledTextCtrl(self, "Clearance"            ,"" , "")
        self.trackw    =LabelledTextCtrl(self, "Track width"            ,"" , "")
        self.viasz     =LabelledTextCtrl(self, "Via Size"            ,"" , "")
        self.viahole   =LabelledTextCtrl(self, "Via Hole"            ,"" , "")
        self.uviasz    =LabelledTextCtrl(self, "µVia Size"            ,"" , "")
        self.uviahole  =LabelledTextCtrl(self, "µVia Hole"            ,"" , "")
        self.dpwidth   =LabelledTextCtrl(self, "DP width"            ,"" , "")
        self.dpgap     =LabelledTextCtrl(self, "DP Gap"            ,"" , "")

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

        self.s.Add(self.dpwidth, 0, wx.ALL  |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)
        self.s.Add(self.dpgap, 0, wx.ALL  |  wx.EXPAND)
        self.s.AddSpacer(WIDGET_SPACING)

        self.SetSizer(self.s)
        self.Layout()
        self.Fit()


def getPcbnewItemByClassAndREName(itype,rename):
    typeclassh = {
        "f":FOOTPRINT,
        "n":NETINFO_ITEM,
        "p":PAD
    }
    iclass = typeclassh[itype]

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
            self.pages = [ PageF(self.nb), PageN(self.nb), PageP(self.nb)]

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
                if(len(sn)):
                    if(sn[:4]!="no_c"):
                        self.currSearch_results[sn] = nbn[n]

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

        return

    def applyfun(self, evt):
        if(self.searchtype == 'p'):
            self.apply_p()
        if(self.searchtype == 'f'):
            self.apply_f()
        if(self.searchtype == 'n'):
            self.apply_n()

        return

    def set_searchre(self, evt):
        self.update_search()
        self.searchre = self.searchre_field.ctrl.GetValue()


    def cancel(self, evt):
        self.searchre = '.'
        #self.searchtype = FOOTPRINT
        self.Close()


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


#
def PinSpektor_callback(evt):

    #debug_dialog("PI CB")
    pin_inspecter = PinSpektorDialog(title="Inspect Pins",tool_tip="",brd=getbrd())

    return

def getbrd():
    return GetBoard()

class PinSpektorPlugin(ActionPlugin):

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
                top_toolbar.Bind(wx.EVT_TOOL, PinSpektor_callback, id=PinSpektor_button)
            except Exception as e:
                debug_dialog("Something went wrong!", e)


            top_toolbar.Realize()
            self.button_inited = True  # Buttons now installed in toolbar.
            pin_inspecter = PinSpektorDialog(title="Inspect Pins",tool_tip="",brd=getbrd())

PinSpektorPlugin().register() # Instantiate and register to Pcbnew
