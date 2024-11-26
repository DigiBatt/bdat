import typing
from datetime import datetime

import bdat.entities as entities
from bdat.database.storage.resource_id import CollectionId
from bdat.database.storage.storage import Storage
from bdat.plots import plot_aging_data
from bdat.tools.cli import print_info


def import_fittingdata(
    storage: Storage, data: dict, project_name: str, target: CollectionId
) -> str:
    raise NotImplementedError()

    # celltypes: typing.Dict[str, entities.BatterySpecies] = {}
    # project = entities.Project(project_name)
    # storage.put(target, project)
    # testset = entities.Testset(name="Fittingdata", project=project)
    # storage.put(target, testset)
    # cellData = []
    # for c in data["cells"]:
    #     print_info(c["name"])
    #     ctypename = c["celltype"]["name"]
    #     if ctypename in celltypes:
    #         ctype = celltypes[ctypename]
    #     else:
    #         ctype = entities.Species(ctypename, "unknown", c["celltype"]["capacity"])
    #         storage.put(target, ctype)
    #         celltypes[ctypename] = ctype
    #     specimen = entities.Specimen(c["name"], project, ctype)
    #     storage.put(target, specimen)
    #     cDate = [
    #         datetime.strptime(date, "%d-%b-%Y %H:%M:%S")
    #         for date in c["capacity"]["index"]
    #     ]
    #     cValue = c["capacity"]["data"]["capacity"]
    #     cAge = c["capacity"]["data"]["age"]
    #     cEfc = c["capacity"]["data"]["efc"]
    #     rDate = [
    #         datetime.strptime(date, "%d-%b-%Y %H:%M:%S")
    #         for date in c["resistance"]["index"]
    #     ]
    #     rValue = c["resistance"]["data"]["resistance"]
    #     rAge = c["capacity"]["data"]["age"]
    #     rEfc = c["capacity"]["data"]["efc"]

    #     if len(rDate) > 0:
    #         minDate = min(cDate[0], rDate[0])
    #         maxDate = min(cDate[-1], rDate[-1])
    #     else:
    #         minDate = cDate[0]
    #         maxDate = cDate[-1]

    #     test = entities.Test(
    #         ahjoId=None,
    #         data=None,
    #         name="Dummy Test",
    #         testset=testset,
    #         specimen=specimen,
    #         startDate=minDate,
    #         equipment=None,
    #         endDate=maxDate,
    #     )
    #     storage.put(target, test)
    #     if c["conditions"]["cRateCharge"] is None:
    #         chargeCurrent = 0
    #     else:
    #         chargeCurrent = c["conditions"]["cRateCharge"] * ctype.capacity
    #     if c["conditions"]["cRateDischarge"] is None:
    #         dischargeCurrent = 0
    #     else:
    #         dischargeCurrent = c["conditions"]["cRateDischarge"] + ctype.capacity
    #     conditions = entities.AgingConditionsEval(
    #         firstStep=0,
    #         lastStep=0,
    #         start=0.0,
    #         end=0.0,
    #         age=0.0,
    #         chargeThroughput=0.0,
    #         temperature=c["conditions"]["temperature"],
    #         dod=c["conditions"]["dod"],
    #         voltage=c["conditions"]["voltage"],
    #         soc=c["conditions"]["soc"],
    #         chargeCurrent=chargeCurrent,
    #         dischargeCurrent=dischargeCurrent,
    #     )
    #     captests = []
    #     for date, cap, age, efc in zip(cDate, cValue, cAge, cEfc):
    #         captest = entities.DischargeCapacityEval(
    #             firstStep=0,
    #             lastStep=0,
    #             start=datetime.timestamp(date),
    #             end=datetime.timestamp(date),
    #             age=age,
    #             chargeThroughput=efc * ctype.capacity,
    #             chargeCurrent=0.0,
    #             eocVoltage=0.0,
    #             cvDuration=0.0,
    #             pauseDuration=0.0,
    #             relaxedVoltage=0.0,
    #             dischargeCurrent=0.0,
    #             dischargeDuration=0.0,
    #             capacity=cap,
    #             eodVoltage=0.0,
    #         )
    #         captests.append(captest)
    #     pulsetests = []
    #     for date, res, age, efc in zip(rDate, rValue, rAge, rEfc):
    #         pulsetest = entities.PulseEval(
    #             firstStep=0,
    #             lastStep=0,
    #             start=datetime.timestamp(date),
    #             end=datetime.timestamp(date),
    #             age=age,
    #             chargeThroughput=efc * ctype.capacity,
    #             relaxationTime=0.0,
    #             current=0.0,
    #             duration=0.0,
    #             relaxedVoltage=0.0,
    #             endVoltage=0.0,
    #             impedance=res,
    #             soc=None,
    #         )
    #         pulsetests.append(pulsetest)
    #     cellLife = entities.CellLife(
    #         cell=specimen,
    #         conditions=[conditions],
    #         capacity=captests,
    #         resistance=pulsetests,
    #     )
    #     storage.put(target, cellLife)
    #     cellData.append(cellLife)
    # agingData = entities.AgingData(cellData)
    # storage.put(target, agingData)
    # agingDataPlot = plot_aging_data(storage, agingData)
    # storage.put(target, agingDataPlot)
    # return agingData.res_id_or_raise().to_str()
