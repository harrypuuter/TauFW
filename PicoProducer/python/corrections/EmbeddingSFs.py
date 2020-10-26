# Author: Sebastian Brommer (October 2020)
import os
from TauFW.PicoProducer import datadir
from RooWorkspaceTool import RooScaleFactor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
pathSFs = os.path.join(datadir, "embedding")


class EmbeddingSFs:
    def __init__(self, era):
        eras = ['2016', '2017', '2018', 'UL2017']
        assert era in eras, "MuonSFs: You must choose a year from: %s." % (
            ', '.join(eras))
        self.era = era
        workspace_dict = {
            "2016": pathSFs + "/Run2016/htt_scalefactors_legacy_2016.root",
            "2017": pathSFs + "/Run2017/htt_scalefactors_legacy_2017.root",
            "2018": pathSFs + "/Run2018/htt_scalefactors_legacy_2018.root"
        }
        self.workspace = workspace_dict[self.era]


class EmbeddingMuonSFs(EmbeddingSFs):
    def __init__(self, era):
        EmbeddingSFs.__init__(self, era)
        """Load workspaces from files."""
        self.arguments = ["m_pt", "m_eta"]
        if self.era == '2016':
            self.sftool_id = RooScaleFactor(workspace=self.workspace,
                                            function="m_id_ratio_emb",
                                            arguments=self.arguments)
            self.sftool_iso = RooScaleFactor(workspace=self.workspace,
                                             function="m_iso_ratio_emb",
                                             arguments=self.arguments)
            self.sftool_trg = RooScaleFactor(workspace=self.workspace,
                                             function="m_trg_ratio_emb",
                                             arguments=self.arguments)
        elif self.era == '2017':
            self.sftool_id = RooScaleFactor(workspace=self.workspace,
                                            function="m_id_embed_kit_ratio",
                                            arguments=self.arguments)
            self.sftool_iso = RooScaleFactor(workspace=self.workspace,
                                             function="m_iso_embed_kit_ratio",
                                             arguments=self.arguments)
            self.sftool_trg = RooScaleFactor(
                workspace=self.workspace,
                function="m_trg24_27_embed_kit_ratio",
                arguments=self.arguments)

        elif self.era == '2018':
            self.sftool_id = RooScaleFactor(workspace=self.workspace,
                                            function="m_id_embed_kit_ratio",
                                            arguments=self.arguments)
            self.sftool_iso = RooScaleFactor(workspace=self.workspace,
                                             function="m_iso_embed_kit_ratio",
                                             arguments=self.arguments)
            self.sftool_trg = RooScaleFactor(
                workspace=self.workspace,
                function="m_trg24_27_embed_kit_ratio",
                arguments=self.arguments)

    def getIdSF(self, pt, eta):
        """Get SF for muon identification."""
        parameters = {'m_pt': pt, 'm_eta': abs(eta)}
        return self.sftool_id.getSF(parameters)

    def getIsoSF(self, pt, eta):
        """Get SF for muon isolation."""
        parameters = {'m_pt': pt, 'm_eta': abs(eta)}
        return self.sftool_iso.getSF(parameters)

    def getTriggerSF(self, pt, eta):
        """Get SF for single muon trigger."""
        parameters = {'m_pt': pt, 'm_eta': abs(eta)}
        return self.sftool_trg.getSF(parameters)


class EmbeddingElectronSFs(EmbeddingSFs):
    def __init__(self, era):
        EmbeddingSFs.__init__(self, era)
        """Load workspaces from files."""
        self.arguments = ["e_pt", "e_eta"]

        if era == '2016':
            self.sftool_id = RooScaleFactor(workspace=self.workspace,
                                            function="e_id_ratio_emb",
                                            arguments=self.arguments)
            self.sftool_iso = RooScaleFactor(workspace=self.workspace,
                                             function="e_iso_ratio_emb",
                                             arguments=self.arguments)
            self.sftool_trg = RooScaleFactor(workspace=self.workspace,
                                             function="e_trg_ratio_emb",
                                             arguments=self.arguments)

        elif era == '2017':
            self.sftool_id = RooScaleFactor(workspace=self.workspace,
                                            function="e_id_embed_kit_ratio",
                                            arguments=self.arguments)
            self.sftool_iso = RooScaleFactor(workspace=self.workspace,
                                             function="e_iso_embed_kit_ratio",
                                             arguments=self.arguments)
            self.sftool_trg = RooScaleFactor(
                workspace=self.workspace,
                function="e_trg27_trg35_embed_kit_ratio",
                arguments=self.arguments)

        elif era == '2018':
            self.sftool_id = RooScaleFactor(workspace=self.workspace,
                                            function="e_id_embed_kit_ratio",
                                            arguments=self.arguments)
            self.sftool_iso = RooScaleFactor(workspace=self.workspace,
                                             function="e_iso_embed_kit_ratio",
                                             arguments=self.arguments)
            self.sftool_trg = RooScaleFactor(
                workspace=self.workspace,
                function="e_trg27_trg35_embed_kit_ratio",
                arguments=self.arguments)

    def getIdSF(self, pt, eta):
        """Get SF for electron identification."""
        parameters = {'e_pt': pt, 'e_eta': abs(eta)}
        return self.sftool_id.getSF(parameters)

    def getIsoSF(self, pt, eta):
        """Get SF for electron isolation."""
        parameters = {'e_pt': pt, 'e_eta': abs(eta)}
        return self.sftool_iso.getSF(parameters)

    def getTriggerSF(self, pt, eta):
        """Get SF for single electron trigger."""
        parameters = {'e_pt': pt, 'e_eta': abs(eta)}
        return self.sftool_trg.getSF(parameters)


class EmbeddingSelectionSFs(EmbeddingSFs):
    def __init__(self, era):
        EmbeddingSFs.__init__(self, era)
        if self.era == "2016":

            self.sftool_seltrg = RooScaleFactor(
                workspace=self.workspace,
                function="m_sel_trg_kit_ratio",
                arguments=["gt1_pt", "gt2_pt", "gt1_eta", "gt2_eta"])
            self.sftool_selid = RooScaleFactor(
                workspace=self.workspace,
                function="m_sel_idemb_kit_ratio",
                arguments=["gt_pt", "gt_eta"])
        else:
            self.sftool_seltrg = RooScaleFactor(
                workspace=self.workspace,
                function="m_sel_trg_ratio",
                arguments=["gt1_pt", "gt2_pt", "gt1_eta", "gt2_eta"])
            self.sftool_selid = RooScaleFactor(workspace=self.workspace,
                                               function="m_sel_idEmb_ratio",
                                               arguments=["gt_pt", "gt_eta"])

    def getEmbeddingSelectionTriggerSF(self, event):
        """Get SF for embedding trigger selection efficiency."""
        parameters = {}
        genparticles = Collection(event, 'GenPart')
        i = 1
        for genparticle in genparticles:
            if abs(genparticle.pdgId) == 15:
                parameters["gt{}_pt".format(i)] = genparticle.pt
                parameters["gt{}_eta".format(i)] = abs(genparticle.eta)
                i += 1
        return self.sftool_seltrg.getSF(parameters)

    def getEmbeddingSelectionIdSF(self, event, index):
        """Get SF for embedding id selection efficiency."""
        parameters = {}
        if index == 1:
            pdgId = 15
        else:
            pdgId = -15
        genparticles = Collection(event, 'GenPart')
        for genparticle in genparticles:
            if genparticle.pdgId == pdgId:
                parameters["gt_pt"] = genparticle.pt
                parameters["gt_eta"] = abs(genparticle.eta)
        return self.sftool_selid.getSF(parameters)