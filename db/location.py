from chimerax.core.commands import run
from chimerax.core.session import Session
from chimerax.core.logger import StringPlainTextLog
import re
import csv

# ========================== PARAMETERS ==========================
mutations = ["p.Val470Met", "p.Arg75Gln", "p.Arg668Cys", "p.Gly576Ala", "p.Ser1235Arg", "p.Glu217Gly", "p.Ile556Val", "p.Leu997Phe", "p.Val754Met", "p.Arg74Trp", "p.Ile148Thr", "p.Arg31Cys", "p.Asp1270Asn", "p.Arg117His", "p.Ser912Leu", "p.Gln1352His", "p.Phe508Cys", "p.Leu967Ser", "p.Arg1162Leu", "p.Ile125Thr", "p.Phe1052Val", "p.Arg297Gln", "p.Ala1285Val", "p.Leu320Val", "p.Arg1070Gln", "p.Ile807Met", "p.Arg170His", "p.Asp836Tyr", "p.Ile285Phe", "p.Arg352Trp", "p.Asp1445Asn", "p.Asp1152His", "p.Ile506Val", "p.Ser895Asn", "p.Phe834Leu", "p.Pro750Leu", "p.Ile1027Thr", "p.Arg1097Cys", "p.Leu183Ile", "p.Gly1069Arg", "p.Tyr301Cys", "p.Tyr1014Cys", "p.Arg74Gln", "p.Met952Thr", "p.Asp443Tyr", "p.Val201Met", "p.Arg117Cys", "p.Val456Ala", "p.Gly551Asp", "p.Leu206Trp", "p.Asn1224Lys", "p.Thr351Ser", "p.Thr438Ala", "p.Arg258Gly", "p.Phe315Ser", "p.Pro140Ser", "p.Thr388Met", "p.Val11Ile", "p.Val520Ile", "p.Val855Ile", "p.Lys68Glu", "p.Val562Ile", "p.Asn1303Lys", "p.Ala120Thr", "p.Glu681Val", "p.Met348Lys", "p.Val920Met", "p.Arg1453Trp", "p.Arg1453Gln", "p.Gly622Asp", "p.Leu1156Phe", "p.Asn287Lys", "p.Phe693Leu", "p.Ala349Val", "p.Ser42Phe", "p.Arg334Gln", "p.Ala399Val", "p.Thr1220Ile", "p.Ile1139Val", "p.Arg851Gln", "p.Glu725Lys", "p.Thr360Ile", "p.Leu986Pro", "p.Thr760Met", "p.Asp924Asn", "p.Arg1162Gln", "p.Arg792Gly", "p.Tyr569Asp", "p.Ala1009Thr", "p.Gly424Ser", "p.Ser549Asn", "p.Gly404Arg", "p.His1375Asn", "p.Gly239Arg", "p.Lys536Glu", "p.Met952Ile", "p.Glu282Asp", "p.Gln151Lys", "p.Tyr919Cys", "p.Ser686Tyr", "p.Ser158Asn", "p.Ser945Leu", "p.Ile507Val", "p.Pro111Leu", "p.Gln1352His", "p.Gly934Ser", "p.Ala455Val", "p.Ser4Leu", "p.Arg334Trp", "p.Phe1337Val", "p.Val562Leu", "p.Ser485Cys", "p.Arg31His", "p.Glu479Asp", "p.Met952Ile", "p.Ala455Glu", "p.Gly1173Ser", "p.Arg1070Trp", "p.Cys866Tyr", "p.Ser485Thr", "p.Arg170Cys", "p.Pro731Leu", "p.Ser256Gly", "p.Asn1303Ile", "p.Arg297Trp", "p.Ala309Gly", "p.Ala46Val", "p.Ser895Thr", "p.Ile853Val", "p.Glu407Lys", "p.Leu130Val", "p.Gly1343Ser", "p.Ile1366Phe", "p.Gly1237Asp", "p.Glu279Asp", "p.Lys14Ile", "p.Gly85Glu", "p.Arg31Leu", "p.Leu889Phe", "p.Ala1136Thr", "p.Leu467Phe", "p.Pro477Ser", "p.Val322Met", "p.Phe316Leu", "p.Arg668His", "p.Leu375Phe", "p.Ser1426Phe", "p.Lys1041Gln", "p.Ile618Thr", "p.Ile269Thr", "p.Thr1057Ala", "p.Gly544Ser", "p.Pro67Leu", "p.Met1137Val", "p.Cys491Phe", "p.Ile1051Val", "p.Arg1422Trp", "p.Ser35Leu", "p.Val12Ala", "p.Asp979Ala", "p.Ala1364Val", "p.Thr854Ile", "p.Val1153Glu", "p.Val43Ile", "p.Arg1066His", "p.Phe650Leu", "p.Pro1013His", "p.Gln715His", "p.Gly213Glu", "p.Ile783Val", "p.Gly817Val", "p.Ser431Gly", "p.Asn287Ser", "p.Ile1230Thr", "p.Arg1066Cys", "p.Asp651Asn", "p.Ala1256Val", "p.Gly1130Ala", "p.Thr887Pro", "p.Pro1013Leu", "p.Asp891Gly", "p.Met469Ile", "p.Cys832Tyr", "p.Asn847Ser", "p.Leu233Val", "p.Cys1395Phe", "p.Val43Ala", "p.Ile119Val", "p.Gly723Val", "p.Thr338Ile", "p.Arg785Gln", "p.Arg792Gln", "p.Asp614Gly", "p.Ile444Thr", "p.Lys411Glu", "p.Asn418Ser", "p.Val171Ile", "p.Lys1080Arg", "p.Pro718Arg", "p.Met1354Thr", "p.Asn965Lys", "p.Arg751Cys", "p.Met156Val", "p.Val1198Met", "p.Ala559Thr", "p.Lys1174Thr", "p.Tyr84His", "p.Arg347His", "p.Ile991Val", "p.Pro5Leu", "p.Tyr1092His", "p.Cys1344Ser", "p.Lys951Glu", "p.Arg560Thr", "p.Glu527Gly", "p.Glu1433Lys", "p.Ala309Thr", "p.Arg352Gln", "p.Arg347Pro", "p.Val232Asp", "p.Val920Leu", "p.Val938Leu", "p.Asn416Ser", "p.Glu528Lys", "p.Arg21Ile", "p.Arg117Gly", "p.Phe1257Leu", "p.Met1354Ile", "p.Met212Val", "p.Arg810Gly", "p.Glu826Lys", "p.Ala252Pro", "p.Val1293Ile", "p.Ser158Thr", "p.Ile752Ser", "p.Glu588Lys", "p.Ala1217Val", "p.Gln1411Pro", "p.Ile132Val", "p.Asn396Tyr", "p.Ile539Thr", "p.Arg1097His", "p.Asp112Gly", "p.Asp110His", "p.Met645Thr", "p.Met1?", "p.Thr896Ile", "p.Pro499Ala", "p.Pro960Ser", "p.Leu214Val", "p.Thr164Ala", "p.Val1421Leu", "p.Ile177Phe", "p.Glu60Asp", "p.Phe1099Leu", "p.Met1101Lys", "p.Ile1131Val", "p.Met645Lys", "p.Ile1328Thr", "p.Leu327Arg", "p.Thr908Asn", "p.His949Leu", "p.Met142Thr", "p.Ile1203Phe", "p.Lys447Arg", "p.Glu449Gly", "p.Thr1299Ala", "p.Ala280Ser", "p.Glu588Gly", "p.Pro676Ala", "p.Phe575Tyr", "p.Gly178Arg", "p.Gln179Lys", "p.Arg1403Lys", "p.Thr1478Arg", "p.Ala534Glu", "p.Val1108Leu", "p.Lys26Glu", "p.Tyr1032Cys", "p.Asp1270Gly", "p.Ala1466Ser", "p.Phe78Tyr", "p.Asp110Glu", "p.Pro888His", "p.Lys978Arg", "p.Gly1349Ser", "p.Val905Leu", "p.Val938Gly", "p.Val603Ile", "p.Met265Arg", "p.Met281Thr", "p.Met152Leu", "p.Ser573Phe", "p.Tyr84Cys", "p.Arg117Leu", "p.Thr94Ile", "p.Ile1002Phe", "p.Asn306Ser", "p.Thr351Ile", "p.Gln1352Glu", "p.Ala221Val", "p.Thr599Ser", "p.Val260Gly", "p.Gly437Asp", "p.Asn423Lys", "p.Ala412Ser", "p.Asn287Tyr", "p.Ile285Thr", "p.Arg751His", "p.Asn1229Lys", "p.Asn699Lys", "p.Pro676Ser", "p.Thr291Arg", "p.Asp674Gly", "p.Ala561Glu", "p.Phe191Val", "p.Ser18Gly", "p.Arg170Ser", "p.Ser1118Phe", "p.Ile705Val", "p.Gln1309Glu", "p.Arg1422Gln", "p.His1054Gln", "p.Pro1290Leu", "p.Leu172Ile", "p.Ser1188Pro", "p.Trp401Cys", "p.Trp401Leu", "p.Glu56Lys", "p.Ser557Thr", "p.Ile1167Val", "p.Leu88Phe", "p.Thr135Ser", "p.Ser1426Pro", "p.Ile86Val", "p.Thr382Pro", "p.Asn1432Lys", "p.Gly126Asp", "p.Val540Ile", "p.Thr547Ile", "p.Gly970Asp", "p.Tyr38His", "p.Gly542Glu", "p.Ala1067Val", "p.Ile1151Val", "p.Asn1148Lys", "p.Arg1102Lys", "p.Ile1023Val", "p.Leu1254Phe", "p.Lys1080Gln", "p.Val1022Met", "p.Ser977Phe", "p.Ser977Ala", "p.Thr1086Ser", "p.Gln353His", "p.Arg347Cys", "p.Ser737Phe", "p.Cys1355Gly", "p.Met469Val", "p.His897Tyr", "p.Phe508Val", "p.Ile1366Thr", "p.His484Tyr", "p.Gln237Glu", "p.Met243Thr", "p.Val915Leu", "p.Ala209Ser", "p.Gln207His", "p.Gly451Arg", "p.Leu159Ser", "p.Asp373Asn", "p.Leu636Pro", "p.Glu1228Gln", "p.Thr291Ile", "p.Lys564Arg", "p.Leu180Val", "p.Thr1171Ala", "p.Phe1413Leu", "p.Leu138Pro", "p.Tyr122Cys", "p.Ser1444Phe", "p.Val1475Met", "p.Val1153Met", "p.Arg75Leu", "p.Lys68Asn", "p.Phe994Leu", "p.Leu1335Phe", "p.Leu467Pro", "p.Leu320Phe", "p.Tyr325Cys", "p.Ser877Ala", "p.Trp57Arg", "p.Arg1422Pro", "p.Glu144Lys", "p.Arg450Ile", "p.Asp1394Gly", "p.Asp806Gly", "p.Gln799Lys", "p.Pro798Ser", "p.Leu796Pro", "p.His775Tyr", "p.Arg764Gln", "p.Ile255Asn", "p.Ile616Val", "p.Met595Val", "p.Cys592Tyr", "p.Leu610Ile", "p.His620Arg", "p.Arg258Ile", "p.Leu259Phe", "p.Pro439Thr", "p.Ile448Thr", "p.Tyr625Asn", "p.Leu435Pro", "p.Gly404Val", "p.Gln1238Lys", "p.Leu633Ile", "p.Val272Ala", "p.Pro1306Ser", "p.Phe1300Leu", "p.Leu1304Val", "p.Gln1382Lys", "p.Ala1225Val", "p.Asp674Val", "p.Pro1050Ala", "p.Arg1385Gly", "p.Arg153Lys", "p.Gly1208Asp", "p.Pro638Ser", "p.Met150Ile", "p.Pro574His", "p.Ile1203Val", "p.Pro704Leu", "p.Thr1053Ile", "p.Tyr563Asn", "p.Asp572Glu", "p.His1197Leu", "p.Asp1312Gly", "p.His147Gln", "p.Gln1291His", "p.Ala747Val", "p.Thr1396Pro", "p.Ile1398Ser", "p.His139Pro", "p.Ser176Thr", "p.Ile177Thr", "p.Pro140Arg", "p.Glu379Asp", "p.Asp1168Gly", "p.Tyr89Cys", "p.Ser707Cys", "p.Cys1410Trp", "p.Tyr380Cys", "p.Arg1479Lys", "p.Ser1426Tyr", "p.Ala300Gly", "p.Ile708Thr", "p.Gln744Pro", "p.Arg709Gln", "p.Phe131Leu", "p.Phe1111Leu", "p.Gly126Ser", "p.Ser549Arg", "p.Leu24Val", "p.Gly542Arg", "p.Tyr38Asn", "p.Gln39His", "p.Val1475Leu", "p.Arg117Ser", "p.Ile1269Met", "p.Leu32Met", "p.Ile1441Thr", "p.Val1272Glu", "p.Gln1268Arg", "p.Gly1244Glu", "p.Cys524Arg", "p.Phe81Leu", "p.Ile1464Thr", "p.Trp361Arg", "p.Thr1263Ile", "p.Met1028Val", "p.Ala1025Ser", "p.Met1028Arg", "p.Phe1450Ile", "p.Gln98Arg", "p.Val1322Phe", "p.Ser1455Ala", "p.Pro740Leu", "p.Ala1081Gly", "p.Ser1251Asn", "p.Asp648Asn", "p.Pro99Leu", "p.Trp1098Cys", "p.Phe976Ser", "p.Ala1018Thr", "p.Pro355Leu", "p.Phe1090Leu", "p.Phe1016Ser", "p.Met1137Thr", "p.Tyr1092Cys", "p.Phe992Leu", "p.Phe310Leu", "p.Ile991Met", "p.Leu1091Phe", "p.Arg104Gly", "p.Ile980Lys", "p.Arg3Met", "p.Met1?", "p.Ser1347Asn", "p.Tyr515His", "p.Cys1355Phe", "p.Pro1372Leu", "p.Leu333Phe", "p.Phe508Leu", "p.Ile506Thr", "p.Asn894Lys", "p.Ser1362Asn", "p.Leu1369Phe", "p.Ile506Leu", "p.Ile331Asn", "p.Gly500Asp", "p.Asp1370Gly", "p.Ile502Thr", "p.Ile502Val", "p.Arg248Thr", "p.Val862Leu", "p.Ala959Val", "p.Ser492Phe", "p.Met961Thr", "p.Ile907Ser", "p.His954Tyr", "p.Arg242Lys", "p.Pro936Thr", "p.Val938Leu", "p.Gly226Glu", "p.Ala204Thr",
             "p.Ala876Val", "p.Met281Val", "p.Ser1311Arg", "p.Arg1158Gln", "p.Pro1290Thr", "p.Lys1165Arg", "p.Thr1036Asn", "p.Asn538Lys", "p.Gly1241Asp", "p.Lys64Glu", "p.Ile1277Val", "p.Phe653Val", "p.Gln1071Arg", "p.Val97Ala", "p.Ser1255Thr", "p.Phe976Leu", "p.Val520Phe", "p.Phe1331Leu", "p.Leu1346Gln", "p.Pro936Leu", "p.Val938Met", "p.His939Asp", "p.Gln220Pro", "p.Phe200Leu", "p.Leu926Phe", "p.Ala561Ser", "p.Gly500Ser", "p.Met1?", "p.Ser589Thr", "p.Lys1080Glu", "p.Ala9Val", "p.Cys225Tyr", "p.Ala1146Val", "p.Gly480Cys", "p.Glu583Gly", "p.Gln493Arg", "p.Gly126Val", "p.His1054Tyr", "p.Val1163Gly", "p.Gly1249Glu", "p.Arg334Leu", "p.Glu384Asp", "p.Arg553Gln", "p.Ser821Asn", "p.Ile661Met", "p.Thr1380Ile", "p.Ser138Asn", "p.Glu54Gly", "p.Phe400Ser", "p.Val922Gly", "p.Gly134Ala", "p.Gly152Arg", "p.Tyr38Cys", "p.Gly149Glu", "p.Asn187Lys", "p.Ala534Ser", "p.Val944Ala", "p.Leu964Phe", "p.Lys1461Glu", "p.Phe87Ser", "p.Gln1330Glu", "p.Glu144Asp", "p.Gly253Glu", "p.Asn801Tyr", "p.Lys946Glu", "p.Ile546Phe", "p.Tyr155Asn", "p.Ala800Ser", "p.Leu802Phe", "p.Ala800Val", "p.Val794Leu", "p.Val794Leu", "p.Arg811Ser", "p.Arg785Pro", "p.Lys786Asn", "p.Gln781His", "p.Glu823Asp", "p.Asp828Asn", "p.Glu826Asp", "p.Ser776Leu", "p.Asp828Glu", "p.His775Arg", "p.Val769Ile", "p.Ser768Phe", "p.Ala252Ser", "p.Gln767His", "p.Gly253Arg", "p.Arg766Lys", "p.Arg765Lys", "p.Ile255Val", "p.Leu617Phe", "p.Asn597Lys", "p.Met595Leu", "p.Ser256Asn", "p.Leu610Phe", "p.Ile601Val", "p.Ile601Phe", "p.His620Leu", "p.Glu257Ala", "p.Ser605Pro", "p.Thr760Arg", "p.Leu259Val", "p.Val260Met", "p.Val260Ala", "p.Gln452Arg", "p.Leu441Pro", "p.Val440Ala", "p.Ile444Val", "p.Asp443Glu", "p.Cys190Ser", "p.Ala462Val", "p.Thr757Ser", "p.Leu188Phe", "p.Ser459Phe", "p.Gly628Arg", "p.Tyr627Cys", "p.Phe626Leu", "p.Cys187Ser", "p.Cys187Gly", "p.His186Gln", "p.Ser756Cys", "p.Thr629Ala", "p.Glu185Val", "p.Leu428Ile", "p.Arg183Lys", "p.Gly404Ala", "p.Val1293Leu", "p.Gly406Glu", "p.Glu407Val", "p.Phe409Ile", "p.Gln414Pro", "p.Tyr161Cys", "p.Asn416Asp", "p.Ile755Phe", "p.Ile160Val", "p.Gln290Arg", "p.Ile1234Val", "p.Lys273Gln", "p.Gly691Arg", "p.Lys273Met", "p.Lys688Gln", "p.Ser686Thr", "p.Thr690Ala", "p.Ser753Gly", "p.Ser753Asn", "p.Glu695Gly", "p.Asn635Thr", "p.Cys276Phe", "p.Lys684Thr", "p.Ser158Cys", "p.Gly1047Val", "p.Lys283Arg", "p.Arg751Leu", "p.Asp373Tyr", "p.Asn1303Tyr", "p.Glu588Ala", "p.Ile1230Val", "p.Asp373Val", "p.Phe587Val", "p.Phe587Ile", "p.Glu585Lys", "p.Tyr1381His", "p.Ala675Val", "p.Glu1228Gly", "p.Tyr1381Ser", "p.Tyr1381Cys", "p.Leu1227Ser", "p.Ser1049Asn", "p.Gln1382His", "p.Thr291Ala", "p.Glu672Lys", "p.Ile1226Thr", "p.Ile154Thr", "p.Thr582Ser", "p.Gly1223Arg", "p.Glu193Gly", "p.Glu193Lys", "p.Val1415Gly", "p.Val1415Asp", "p.Arg1386Gly", "p.His667Tyr", "p.Ile1051Phe", "p.Thr1216Ala", "p.Tyr1219His", "p.Leu293Met", "p.Asp579Gly", "p.Gln1209Lys", "p.Met152Ile", "p.Gln151Arg", "p.Gln151Pro", "p.Met1210Leu", "p.Arg560Ser", "p.Asn703Ile", "p.Gly576Val", "p.Tyr577Cys", "p.Tyr577Phe", "p.Phe575Ile", "p.Phe1052Leu", "p.Ala566Asp", "p.Pro704Arg", "p.Leu188Pro", "p.Asp565His", "p.Asp565Tyr", "p.Asp1201Tyr", "p.Lys564Glu", "p.Phe1392Leu", "p.Asp567Asn", "p.Tyr1307Asn", "p.Ser1118Cys", "p.Ser573Cys", "p.Lys1200Gln", "p.Val1198Leu", "p.Lys1199Arg", "p.His1197Arg", "p.Lys52Ile", "p.Met1157Ile", "p.Gln1313Lys", "p.Val1318Ala", "p.Val1318Ile", "p.Trp1310Gly", "p.Gln378Arg", "p.Asp1394His", "p.Asn1419Lys", "p.Ile1117Thr", "p.Val1421Met", "p.Ser1159Pro", "p.Ser1159Phe", "p.Ter1481Tyr", "p.Met1191Thr", "p.His147Asn", "p.Gln1291Arg", "p.Ala559Ser", "p.Ser1188Leu", "p.Phe1116Ser", "p.Phe17Leu", "p.Thr1396Arg", "p.Gly91Arg", "p.Ile661Val", "p.Ile661Thr", "p.Ile371Met", "p.Leu1187Val", "p.Leu1187Ile", "p.Ile1289Val", "p.Ala141Thr", "p.Gln1186His", "p.Ile371Thr", "p.Leu49Pro", "p.Leu558Ser", "p.Gly178Glu", "p.Glu527Gln", "p.Asn1184Lys", "p.Ser176Asn", "p.Lys1183Asn", "p.Asn48Lys", "p.Ser176Arg", "p.Val1114Leu", "p.Leu1480Pro", "p.Ile177Met", "p.Glu1172Gln", "p.Ile177Val", "p.Ala299Thr", "p.Pro1181Gln", "p.Val1288Ala", "p.His139Tyr", "p.Tyr1182His", "p.Lys370Glu", "p.Arg1403Gly", "p.Leu15Phe", "p.Leu15Val", "p.Arg1283Lys", "p.Lys1177Arg", "p.Lys1177Thr", "p.Cys1410Ser", "p.Glu1044Gln", "p.Ser641Gly", "p.Arg553Pro", "p.Glu1409Lys", "p.Leu88Ser", "p.Asp58His", "p.Asn369Ser", "p.Ala399Gly", "p.Thr1478Ile", "p.Asp44Val", "p.Asp58Gly", "p.Asp58Val", "p.Gly1061Arg", "p.Leu1279Trp", "p.Lys14Arg", "p.Gly551Ser", "p.Glu656Gln", "p.Ile132Thr", "p.Thr20Ser", "p.Val43Leu", "p.Ile530Met", "p.Lys14Glu", "p.Thr20Ser", "p.Gln1281Arg", "p.Gln1039Arg", "p.Asp1154Glu", "p.Ala1067Thr", "p.Lys532Asn", "p.Trp1282Cys", "p.Arg1438Trp", "p.Leu548Pro", "p.Leu1065Phe", "p.Ile530Asn", "p.Val540Ala", "p.Ser654Gly", "p.Ala120Ser", "p.Ser549Arg", "p.Phe83Leu", "p.Leu1431Arg", "p.Ile121Phe", "p.Asn396Thr", "p.Gln652Glu", "p.Gln652Lys", "p.Asp1154Gly", "p.Arg29Thr", "p.Asn538Tyr", "p.Ile37Val", "p.Thr94Pro", "p.Thr547Ala", "p.Ala1440Thr", "p.Thr390Ile", "p.Val1240Gly", "p.Ile1109Val", "p.Ser1442Arg", "p.Ser1442Arg", "p.Met394Thr", "p.Leu1242Phe", "p.Leu32Pro", "p.Ser118Phe", "p.Ser118Cys", "p.Tyr28His", "p.Thr390Ala", "p.Pro1443Ser", "p.Pro1443Ala", "p.Leu1436Phe", "p.Ala1031Val", "p.Met1028Ile", "p.Lys65Arg", "p.Ala72Thr", "p.Leu387Ser", "p.Val1272Gly", "p.Ile1106Thr", "p.Ile1441Val", "p.Val11Leu", "p.Ser1248Leu", "p.Thr389Ser", "p.Thr1246Ile", "p.Thr1246Ser", "p.Ile1277Thr", "p.Val11Ala", "p.Gly1244Val", "p.Trp79Arg", "p.Leu1029Met", "p.Gly1249Arg", "p.Glu116Gln", "p.Cys76Trp", "p.Phe78Leu", "p.Leu73Phe", "p.Ser10Arg", "p.Ala1025Val", "p.Cys76Arg", "p.Glu116Gly", "p.Glu116Ala", "p.Ala1146Asp", "p.Glu1264Gly", "p.Ser10Asn", "p.Ser1255Leu", "p.Arg1259Thr", "p.Phe1074Leu", "p.Phe1074Leu", "p.Lys1457Asn", "p.Phe305Val", "p.Val1322Ile", "p.Asp112Asn", "p.Arg1097Pro", "p.Gly1130Val", "p.Ser1251Arg", "p.Ile1023Arg", "p.Met1101Ile", "p.Ile995Asn", "p.Gly1130Ser", "p.Val1147Glu", "p.Ile995Leu", "p.Leu1077Pro", "p.Phe994Cys", "p.Pro1021Thr", "p.Pro1021Ser", "p.Asp110Tyr", "p.Ile521Leu", "p.Ile521Phe", "p.Thr887Asn", "p.Phe976Leu", "p.Glu7Gln", "p.Gln1100Pro", "p.His1085Pro", "p.Leu102Arg", "p.Ser977Cys", "p.Val1001Leu", "p.Ser977Pro", "p.Val1327Leu", "p.Asp993Gly", "p.Ile1328Met", "p.Tyr109Asn", "p.Gly1003Glu", "p.Thr1086Ala", "p.Ala1004Gly", "p.Val714Leu", "p.Leu889Val", "p.Trp1089Cys", "p.Ile1328Val", "p.Ser519Asn", "p.Ser4Ala", "p.Phe992Leu", "p.Pro1013Arg", "p.Ala1006Thr", "p.Ile105Val", "p.Met348Val", "p.Ala1006Glu", "p.Thr990Asn", "p.Thr990Ser", "p.Leu6Arg", "p.Asp979Gly", "p.Leu1339Pro", "p.Arg347Ser", "p.Asp1341Gly", "p.Met1140Val", "p.Phe1331Ile", "p.Val1008Asp", "p.Pro1378Leu", "p.Val1379Leu", "p.Asp985Asn", "p.Ile1005Arg", "p.Gly1343Ala", "p.Gly1343Asp", "p.Ile982Val", "p.Asp984Asn", "p.Asp985Glu", "p.Ala1009Val", "p.Asp1377Asn", "p.Asp1377His", "p.Asp513Gly", "p.Asp513Tyr", "p.Gln890Arg", "p.Ile344Val", "p.Thr465Asn", "p.Asp891Asn", "p.Ser466Leu", "p.Lys1351Asn", "p.Cys343Phe", "p.Val510Ile", "p.His1375Arg", "p.Ile340Val", "p.Gly314Glu", "p.Ile336Lys", "p.Ile336Thr", "p.Phe337Val", "p.Thr338Ala", "p.Ser737Thr", "p.Met469Ile", "p.Glu873Val", "p.Gln720Arg", "p.Ser1359Cys", "p.Lys1363Arg", "p.Pro477Thr", "p.Asn894Ser", "p.Arg1358Gly", "p.Ser1362Thr", "p.Leu1361Val", "p.Asp1370His", "p.Ile471Val", "p.Val317Gly", "p.Ser321Pro", "p.Glu474Gln", "p.Cys832Gly", "p.Ile1366Asn", "p.Asp727Ala", "p.Pro499Ser", "p.Ser898Arg", "p.Glu479Gly", "p.Arg248Lys", "p.Asn901Ile", "p.Met961Ile", "p.Leu859Phe", "p.Ser495Phe", "p.Lys857Asn", "p.Arg487Lys", "p.Tyr903Cys", "p.Met498Thr", "p.Tyr849Cys", "p.Pro960Leu", "p.Met837Thr", "p.Ala959Thr", "p.Ile853Phe", "p.Phe490Cys", "p.Met961Val", "p.Ile907Val", "p.Thr910Ser", "p.Ser911Asn", "p.His949Tyr", "p.Met244Val", "p.Met244Ile", "p.Lys951Thr", "p.Met243Val", "p.Leu948Phe", "p.His950Arg", "p.Ala234Ser", "p.Tyr913Cys", "p.Gly241Arg", "p.Lys946Gln", "p.Ile918Val", "p.His939Gln", "p.Gly921Arg", "p.Gly194Val", "p.Phe229Tyr", "p.Phe236Ser", "p.Leu926Ser", "p.Phe224Leu", "p.Gly226Val", "p.Thr925Asn", "p.Ala204Ser", "p.Ala196Val", "p.Pro205Ser", "p.Ala198Val", "p.Pro205Leu", "p.Val208Ala", "p.Ala198Pro", "p.Leu210Phe", "p.His199Arg", "p.Phe200Ile", "p.Glu217Lys", "p.Trp216Arg", "p.Val874Leu"]


structures = [
    "5UAK", "5W81", "5UAR", "6MSM", "6O1V", "6O2P", "7SVR", "7SVD", "7SV7", "8EJ1", "8EIG", "8EIQ", "8EIO", "8FZQ"
]
output_csv_path = "./DATA/NEWNEWNEW.csv"

# ========================== DATA EXTRACTION ==========================


def extract_section(log_output, start_marker, end_marker):
    section_data = []
    in_section = False
    for line in log_output.splitlines():
        if start_marker in line:
            in_section = True
            continue
        if end_marker in line:
            break
        if in_section:
            section_data.append(line.strip())
    return section_data


def extract_atoms(log_output):
    atom_data = []
    atom_pattern = re.compile(r'atom id (/A:(\d+)@(\S+)) idatm_type')

    for match in atom_pattern.finditer("\n".join(extract_section(log_output, "--start-atoms--", "--end-atoms--"))):
        full_id, residue_num, atom_name = match.groups()
        atom_data.append((int(residue_num), atom_name, full_id))

    atom_priority = ["CA", "N", "CB", "CG1", "CG2", "CD", "CE"]
    best_atoms = {}

    for residue, atom_name, full_id in atom_data:
        if residue not in best_atoms:
            best_atoms[residue] = (atom_name, full_id)
        else:
            current_best = best_atoms[residue][0]
            if atom_name in atom_priority and (
                current_best not in atom_priority or atom_priority.index(
                    atom_name) < atom_priority.index(current_best)
            ):
                best_atoms[residue] = (atom_name, full_id)

    return [atom_id for _, atom_id in best_atoms.values()]


def extract_distances(log_output):
    print(f"[DEBUG] Raw log before extraction:\n{log_output}")

    distance_pattern = re.compile(r"Distance between .*?: ([\d\.]+)Å")
    matches = distance_pattern.findall("\n".join(extract_section(
        log_output, "--start-distance--", "--end-distance--")))

    distances = [float(match) for match in matches] if matches else []

    print(f"[DEBUG] Extracted raw distances: {distances}")
    return distances

# ========================== STRUCTURE VALIDATION ==========================


def check_ligands():
    with StringPlainTextLog(session.logger) as log:
        run(session, "select ligand")
        run(session, "info selection")
        log_output = log.getvalue()
    return "No atoms selected" not in log_output

# ========================== DISTANCE CALCULATION ==========================


def compute_distances(atom_list1, atom_list2, structure, mutation):
    count_in_range = 0

    print(
        f"\n[DEBUG] Computing distances between {len(atom_list1)} and {len(atom_list2)} atoms for {structure}_{mutation}...")

    if not atom_list1 or not atom_list2:
        print(
            f"[ERROR] One of the atom lists is empty! Skipping distance calculations for {structure}_{mutation}.")
        return 0

    # Delete existing distance measurements to avoid conflicts
    run(session, "distance delete all")

    with StringPlainTextLog(session.logger) as log:
        run(session, "log text --start-distance--")

        measured_pairs = set()  # To keep track of already measured distances

        for atom1 in atom_list1:
            for atom2 in atom_list2:
                if atom1 == atom2 or (atom1, atom2) in measured_pairs or (atom2, atom1) in measured_pairs:
                    print(
                        f"[DEBUG] Skipping duplicate/self-distance: {atom1} to {atom2}")
                    continue

                print(f"[DEBUG] Measuring distance: {atom1} to {atom2}")
                run(session, f"distance {atom1} {atom2}")
                # Store the pair to prevent duplicate calculations
                measured_pairs.add((atom1, atom2))

        run(session, "log text --end-distance--")

        log_output = log.getvalue()
        distance_values = extract_distances(log_output)

        for d in distance_values:
            print(f"[DEBUG] Checking distance {d}Å for {structure}_{mutation}")
            if d < 5.0:
                print(
                    f"[DEBUG] ✅ Distance under 5Å: {d}Å for {structure}_{mutation}")
                count_in_range += 1

    print(
        f"[DEBUG] Finished computing distances for {structure}_{mutation}. Found {count_in_range} pairs under 5Å.")
    return count_in_range


# ========================== MAIN PROCESSING ==========================

def process_structure(structure, mutation):
    print(
        f"\n========== Processing {structure} with mutation {mutation} ==========")
    residue_number = re.search(r'\d+', mutation).group()

    print(f"[DEBUG] Opening structure {structure}...")
    run(session, f"open {structure}")

    print(f"[DEBUG] Checking for ligands in {structure}...")
    if not check_ligands():
        print(f"[DEBUG] No ligands found in {structure}. Skipping...")
        run(session, "close all")
        return 0

    print(f"[DEBUG] Selecting atoms within 4.5Å of ligand...")
    try:
        with StringPlainTextLog(session.logger) as log:
            run(session, "log text --start-atoms--")
            run(session, "select zone ligand 4.5 protein residues true;")
            run(session, "info atoms sel")
            run(session, "log text --end-atoms--")
            log_output = log.getvalue()

        if "No atoms selected" in log_output:
            print(
                f"[DEBUG] No atoms found in 4.5Å ligand zone for {structure}. Skipping...")
            run(session, "close all")
            return 0

        atom_list1 = extract_atoms(log_output)
        print(
            f"[DEBUG] Extracted {len(atom_list1)} atoms in 4.5Å zone of ligand.")

    except Exception as e:
        print(
            f"[ERROR] Ligand zone selection failed for {structure}: {str(e)}")
        run(session, "close all")
        return 0

    print(f"[DEBUG] Deselecting all atoms...")
    run(session, "~sel")

    print(
        f"[DEBUG] Selecting atoms near residue {residue_number} in {structure}...")
    try:
        run(session, f"sel :{residue_number}")

        with StringPlainTextLog(session.logger) as log:
            run(session, "log text --start-atoms--")
            run(session, "select sel@<5")
            run(session, "info atoms sel")
            run(session, "log text --end-atoms--")
            log_output = log.getvalue()

        if "No atoms selected" in log_output:
            print(
                f"[DEBUG] No atoms found near mutation site {residue_number} for {structure}. Skipping...")
            run(session, "close all")
            return 0

        atom_list2 = extract_atoms(log_output)
        print(
            f"[DEBUG] Extracted {len(atom_list2)} atoms in 5Å zone of residue {residue_number}.")

    except Exception as e:
        print(
            f"[ERROR] Mutation site selection failed for {structure}: {str(e)}")
        run(session, "close all")
        return 0

    print(
        f"[DEBUG] Starting distance computation between {len(atom_list1)} and {len(atom_list2)} atoms...")
    result = compute_distances(atom_list1, atom_list2, structure, mutation)
    print(
        f"[DEBUG] Finished processing {structure} {mutation}. Found {result} pairs under 5Å.")

    run(session, "close all")

    return result

# ========================== EXECUTION & CSV OUTPUT ==========================


print("Starting analysis...")
results = []

for structure in structures:
    for mutation in mutations:
        count = process_structure(structure, mutation)
        results.append([f"{structure}_{mutation}", count])
        print(f"{structure} {mutation}: {count} atom pairs under 5Å")

with open(output_csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Structure_Mutation", "Pairs"])
    writer.writerows(results)

print(f"Results saved to {output_csv_path}")
print("Analysis complete.")
