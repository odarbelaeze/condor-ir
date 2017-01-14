import pytest

from condor.util import isi_text_to_dic


@pytest.fixture(scope='module')
def isi_text(request):
    return '''
FN Thomson Reuters Web of Science™
VR 1.0
PT J
AU Jeong, K
   Hong, T
   Ban, C
   Koo, C
   Park, HS
AF Jeong, Kwangbok
   Hong, Taehoon
   Ban, Cheolwoo
   Koo, Choongwan
   Park, Hyo Seon
TI Life cycle economic and environmental assessment for establishing the
   optimal implementation strategy of rooftop photovoltaic system in
   military facility
SO JOURNAL OF CLEANER PRODUCTION
LA English
DT Article
DE Photovoltaic (PV) system; Life cycle cost; Life cycle CO2; Military
   facility; Gable roof
ID RENEWABLE ENERGY SYSTEM; EDUCATIONAL FACILITY; SOLAR; COST; ELECTRICITY;
   BUILDINGS; FRAMEWORK; MODEL; OPTIMIZATION; EMISSIONS
AB The Ministry of National Defense (South Korea) promotes its Defense Green \
    Growth policy to reduce greenhouse gas emissions. Based on this background\
, this study aimed to conduct the life cycle economic and environmental\
    assessment for establishing the optimal implementation strategy for \
    rooftop photovoltaic system in military facility. Considering three \
    factors (i.e., the orientation of the gable roof, the installation area of\
    the PV system, and the slope of the installed panel), 12 implementation \
    scenarios of PV system were established. The detailed results by prototype\
    are summarized in terms of the two perspectives (i.e., the absolute and \
    relative investment values): (i) Prototype 1 (south-north): P1-S/N (opt.) \
    in terms of the NPV25 (net present value at year 25) and P1-S (opt.) in \
    terms of the SIR25 (savings-to-investment ratio at year 25); (ii) \
    Prototype 2 (southeast-northwest): P2-SE/NW (opt.) in terms of the NPV25 \
    and P2-SE (ext.) in terms of the SIR25; and (iii) Prototype 3 (east-west):\
    P3-E/W (ext.) in terms of the NPV25 and P3-E (opt.) in terms of the SIR25.\
C1 [Jeong, Kwangbok; Hong, Taehoon; Ban, Cheolwoo; Koo, Choongwan; Park,
RP Hong, T (reprint author), Yonsei Univ, Dept Architectural Engn, Seoul
EM kbjeong7@yonsei.ac.kr; hong7@yonsei.ac.kr; qkscjfdn@naver.com;
   cwkoo@yonsei.ac.kr; hspark@yonsei.ac.kr
FU National Research Foundation of Korea (NRF) grant - Korea government
   (MSIP; Ministry of Science, ICT & Future Planning)
   [NRF-2012R1A2A1A01004376, 2011-0018360]
FX This work was supported by the National Research Foundation of Korea
   (NRF) grant funded by the Korea government (MSIP; Ministry of Science,
   ICT & Future Planning) (NRF-2012R1A2A1A01004376 & No. 2011-0018360).
CR Bravi M, 2014, J CLEAN PROD, V66, P301, DOI 10.1016/j.jclepro.2013.11.015
   CEC (California Energy Commission), 2001, GUID PHOT PV SYST DE
   CRS (Congressional Research Service), 2012, DEP DEF EN IN BACKGR
   Cucchiella F., 2015, J CLEAN PROD, V98, P241
   Dell'lsola A. J., 2003, LIFE CYCLE COSTING F
   Gupta MJ, 2002, ENERGY, V27, P777, DOI 10.1016/S0360-5442(02)00030-0
   Hong T, 2012, ENERG BUILDINGS, V45, P229, DOI 10.1016/j.enbuild.2011.11.006
   Hong T, 2014, RENEW SUST ENERG REV, V29, P286, DOI 10.1016/j.rser.2013.08.0\
61
   Hong T, 2014, ENERGY, V65, P190, DOI 10.1016/j.energy.2013.11.082
   Hong T, 2014, ENERG POLICY, V66, P157, DOI 10.1016/j.enpol.2013.10.057
   Hong T, 2013, APPL ENERG, V103, P539, DOI 10.1016/j.apenergy.2012.10.013
   Jeong K., 2014, J CLEAN PROD, V20, P1
   Ji C, 2014, ENERG BUILDINGS, V72, P186, DOI 10.1016/j.enbuild.2013.12.045
   KCER (Korean Certified Emission Reductions), 2014, KOR VOL EM RED
   KEI (Korea Environment Institute), 2012, INT TRENDS GHG RED P
   KEMCO (Korea Energy Management Corporation), 2014, AUT CALC TOE CO2 EM
   Kim C. J., 2015, ENV IMPACT ASSES, V54, P9
   Kim D, 2014, ENERGIES, V7, P5129, DOI 10.3390/en7085129
   KMKE (Korea Ministry of Knowledge Economy), 2012, REG GOV PROC TRAD ST
   Koo C, 2013, ENVIRON SCI TECHNOL, V47, P4829, DOI 10.1021/es303774a
   Koo C, 2014, PROG PHOTOVOLTAICS, V22, P462, DOI 10.1002/pip.2448
   KURC (Korea Urban Renaissance Center), 2010, 4 ANN RES DEV REP
   Lee M, 2014, ENVIRON SCI TECHNOL, V48, P4604, DOI 10.1021/es405293u
   MND (Ministry of National Defense), 2012, DEF MIL INST STAND
   MND (Ministry of National Defense), 2011, DEF GREEN GROWTH REF
   MND (Ministry of National Defense), 2012, DEF WHIT PAP
   MNR (Ministry of Natural Resources), 2004, CLEAN EN PROJ AN RET
   MNR (Ministry of Natural Resources), 2013, RETSCREEN 4
   Mohamad RS, 2014, J CLEAN PROD, V70, P78, DOI 10.1016/j.jclepro.2014.02.033
   NREL (National Renewable Energy Laboratory), 2011, LESS LEARN NET ZER E
   NREL (National Renewable Energy Laboratory), 2010, 2008 SOL TECHN MARK
   Othman NF, 2015, J CLEAN PROD, V91, P71, DOI 10.1016/j.jclepro.2014.12.044
   Swift KD, 2013, RENEW ENERG, V57, P137, DOI 10.1016/j.renene.2013.01.011
   Uddin MS, 2014, J CLEAN PROD, V69, P153, DOI 10.1016/j.jclepro.2014.01.073
   Urn T. J., 2012, P SAREK 2012 SUMM AN, V6, P301
NR 45
TC 0
Z9 0
PU ELSEVIER SCI LTD
PI OXFORD
PA THE BOULEVARD, LANGFORD LANE, KIDLINGTON, OXFORD OX5 1GB, OXON, ENGLAND
SN 0959-6526
EI 1879-1786
J9 J CLEAN PROD
JI J. Clean Prod.
PD OCT 1
PY 2015
VL 104
BP 315
EP 327
DI 10.1016/j.jclepro.2015.05.066
PG 13
WC Engineering, Environmental; Environmental Sciences
SC Engineering; Environmental Sciences & Ecology
GA CM3AG
UT WOS:000357552900031
ER
'''


def test_isi_record_to_dic(isi_text):
    dic = isi_text_to_dic(isi_text)
    assert ['J'] == dic['PT']
    assert 5 == len(dic['AU'])
