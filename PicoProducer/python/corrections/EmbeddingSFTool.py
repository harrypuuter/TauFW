# Author: Sebastian Brommer (October 2020)
import os
from TauFW.PicoProducer import datadir
from RooWorkspaceTool import RooScaleFactor
pathSFs = os.path.join(datadir, "embedding")


class EmbeddingMuonSFs:
    def __init__(self, era=2017):
        """Load histograms from files."""

        eras = ['2016', '2017', '2018', 'UL2017']
        assert era in eras, "MuonSFs: You must choose a year from: %s." % (
            ', '.join(eras))

        if era == '2016':
            self.sftool_id = RooScaleFactor(
                workspace=pathSFs +
                "/Run2016/htt_scalefactors_legacy_2016.root",
                function="m_id_ratio_emb",
                arguments=["m_pt", "m_eta"])
            self.sftool_iso = RooScaleFactor(
                workspace=pathSFs +
                "/Run2016/htt_scalefactors_legacy_2016.root",
                function="m_iso_ratio_emb",
                arguments=["m_pt", "m_eta"])
            self.sftool_trg = RooScaleFactor(
                workspace=pathSFs +
                "/Run2016/htt_scalefactors_legacy_2016.root",
                function="m_trg_ratio_emb",
                arguments=["m_pt", "m_eta"])

        elif era == '2017':
            self.sftool_id = RooScaleFactor(
                workspace=pathSFs +
                "/Run2017/htt_scalefactors_legacy_2017.root",
                function="m_id_embed_kit_ratio",
                arguments=["m_pt", "m_eta"])
            self.sftool_iso = RooScaleFactor(
                workspace=pathSFs +
                "/Run2017/htt_scalefactors_legacy_2017.root",
                function="m_iso_embed_kit_ratio",
                arguments=["m_pt", "m_eta"])
            self.sftool_trg = RooScaleFactor(
                workspace=pathSFs +
                "/Run2017/htt_scalefactors_legacy_2017.root",
                function="m_trg24_27_embed_kit_ratio",
                arguments=["m_pt", "m_eta"])

        elif era == '2018':
            self.sftool_id = RooScaleFactor(
                workspace=pathSFs +
                "/Run2018/htt_scalefactors_legacy_2018.root",
                function="m_id_embed_kit_ratio",
                arguments=["m_pt", "m_eta"])
            self.sftool_iso = RooScaleFactor(
                workspace=pathSFs +
                "/Run2018/htt_scalefactors_legacy_2018.root",
                function="m_iso_embed_kit_ratio",
                arguments=["m_pt", "m_eta"])
            self.sftool_trg = RooScaleFactor(
                workspace=pathSFs +
                "/Run2018/htt_scalefactors_legacy_2018.root",
                function="m_trg24_27_embed_kit_ratio",
                arguments=["m_pt", "m_eta"])

    def getIdSF(self, pt, eta):
        """Get SF for muon identification."""
        parameters = {'m_pt': pt, 'm_eta': eta}
        return self.sftool_id.getSF(parameters)

    def getIsoSF(self, pt, eta):
        """Get SF for muon isolation."""
        parameters = {'m_pt': pt, 'm_eta': eta}
        return self.sftool_iso.getSF(parameters)

    def getTriggerSF(self, pt, eta):
        """Get SF for single muon trigger."""
        parameters = {'m_pt': pt, 'm_eta': eta}
        return self.sftool_trg.getSF(parameters)
