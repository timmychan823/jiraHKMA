import os
import json
import pandas as pd
from datetime import datetime
from datetime import date
import numpy as np

f = open("IncidentSummaryJson.json")

data = json.load(f)

df = pd.DataFrame(
    columns=[
        "Incident Log No.",
        "Production / UAT",
        "Priority",
        "Incident Type",
        "Server",
        "Description",
        "Reported By",
        "Category",
        "Component / Area",
        "Incident Date",
        "Reported Date",
        "Last Update Date",
        "Status",
    ]
)

for x in data["issues"]:
    # need to find field id for End User Support too
    # incident type, server, end user support, category, component/ area may be None, replace them with "N/A"
    # end user support can be multiple, check check how to handle it
    try:
        incident_type = x["fields"]["customfield_12124"]["value"]
    except KeyError:
        incident_type = "N/A"
    try:
        server = x["fields"]["customfield_10601"]
    except KeyError:
        server = "N/A"
    try:
        category = x["fields"]["customfield_12126"]["value"]
    except KeyError:
        category = "N/A"
    try:
        component_area = x["fields"]["customfield_12126"]["child"]["value"]
    except KeyError:
        component_area = "N/A"

    df = pd.concat(
        [
            df,
            pd.DataFrame(
                {
                    "Incident Log No.": [x["key"]],
                    "Production / UAT": [x["fields"]["issuetype"]["name"]],
                    "Priority": [x["fields"]["priority"]["name"]],
                    "Incident Type": [incident_type],
                    "Server": [server],
                    "Description": [x["fields"]["summary"]],
                    "Reported By": [x["fields"]["creator"]["displayName"]],
                    "Category": [category],
                    "Component / Area": [component_area],
                    "Incident Date": [
                        datetime.strptime(
                            " ".join(x["fields"]["created"].split("T")),
                            r"%Y-%m-%d %H:%M:%S.%f%z",
                        )
                    ],
                    "Reported Date": [
                        datetime.strptime(
                            " ".join(x["fields"]["created"].split("T")),
                            r"%Y-%m-%d %H:%M:%S.%f%z",
                        )
                    ],
                    "Last Update Date": [
                        datetime.strptime(
                            " ".join(x["fields"]["updated"].split("T")),
                            r"%Y-%m-%d %H:%M:%S.%f%z",
                        )
                    ],
                    "Status": [x["fields"]["status"]["name"]],
                }
            ),
        ]
    )


df["Incident Date"] = df["Incident Date"].dt.tz_localize(None)
df["Reported Date"] = df["Reported Date"].dt.tz_localize(None)
df["Last Update Date"] = df["Last Update Date"].dt.tz_localize(None)

prod_df = df[df["Production / UAT"] == "Production Incident"]
uat_df = df[df["Production / UAT"] == "UAT Incident"]


writer = pd.ExcelWriter(
    f"EPSSIncidentLogSummary({date.today().strftime(r'%b_%d_%Y')}).xlsx",
    engine="xlsxwriter",
)

# Convert the dataframe to an XlsxWriter Excel object. Turn off the default
# header and index and skip one row to allow us to insert a user defined
# header.
prod_df.to_excel(writer, sheet_name="PROD", startrow=2, header=False, index=False)

prod_df["Status"] = pd.Categorical(prod_df["Status"])
for status in [
    "Submitted to vendor",
    "Pending for retest",
    "Pending Action by AS Team",
    "Closed",
    "Cancelled",
]:
    if status not in prod_df["Status"].cat.categories:
        prod_df["Status"] = prod_df["Status"].cat.add_categories(status)
    if status not in prod_df["Status"].cat.categories:
        prod_df["Status"] = prod_df["Status"].cat.add_categories(status)

prod_df["Status"] = prod_df["Status"].cat.reorder_categories(
    [
        "Submitted to vendor",
        "Pending for retest",
        "Pending Action by AS Team",
        "Closed",
        "Cancelled",
    ]
)

pivot_prod = (
    pd.pivot_table(
        prod_df,
        values="Incident Log No.",
        index="Priority",
        columns="Status",
        aggfunc="count",
        fill_value=0,
        dropna=False,
    )
    .reset_index()
    .set_index("Priority")
)


pivot_prod.to_excel(writer, sheet_name="PROD_STAT", startcol=0, startrow=1)

uat_df.to_excel(writer, sheet_name="UAT", startrow=2, header=False, index=False)
uat_df["Status"] = pd.Categorical(uat_df["Status"])
for status in [
    "Submitted to vendor",
    "Pending for retest",
    "Pending Action by AS Team",
    "Closed",
    "Cancelled",
]:
    if status not in uat_df["Status"].cat.categories:
        uat_df["Status"] = uat_df["Status"].cat.add_categories(status)
    if status not in uat_df["Status"].cat.categories:
        uat_df["Status"] = uat_df["Status"].cat.add_categories(status)

uat_df["Status"] = uat_df["Status"].cat.reorder_categories(
    [
        "Submitted to vendor",
        "Pending for retest",
        "Pending Action by AS Team",
        "Closed",
        "Cancelled",
    ]
)
pivot_uat = (
    pd.pivot_table(
        uat_df,
        values="Incident Log No.",
        index="Priority",
        columns="Status",
        aggfunc="count",
        fill_value=0,
        dropna=False,
    )
    .reset_index()
    .set_index("Priority")
)


pivot_uat.to_excel(writer, sheet_name="UAT_STAT", startcol=0, startrow=1)

# Get the xlsxwriter workbook and worksheet objects.
workbook = writer.book

incidentDateFormat = workbook.add_format().set_num_format(22)
bold = workbook.add_format({"bold": True})

prod_worksheet = writer.sheets["PROD"]
uat_worksheet = writer.sheets["UAT"]

# Get the dimensions of the dataframe.
(prod_max_row, prod_max_col) = prod_df.shape
(uat_max_row, uat_max_col) = uat_df.shape


prod_worksheet.write(0, 0, "Incident Report Summary List", bold)
prod_worksheet.write(0, 4, f"As of Date: {date.today().strftime(r'%d %b %Y')}", bold)

# Create a list of column headers, to use in add_table().
column_settings = []
for header in prod_df.columns:
    if (
        header == "Incident Date"
        or header == "Reported Date"
        or header == "Last Update Date"
    ):
        column_settings.append({"header": header, "format": incidentDateFormat})
    else:
        column_settings.append({"header": header})

# Add the table.
prod_worksheet.add_table(
    1, 0, prod_max_row + 1, prod_max_col - 1, {"columns": column_settings}
)

# Make the columns wider for clarity.
prod_worksheet.set_column(0, prod_max_col - 1, 20)

uat_worksheet.write(0, 0, "Incident Report Summary List", bold)
uat_worksheet.write(0, 4, f"As of Date: {date.today().strftime(r'%d %b %Y')}", bold)

column_settings = []
for header in prod_df.columns:
    if (
        header == "Incident Date"
        or header == "Reported Date"
        or header == "Last Update Date"
    ):
        column_settings.append({"header": header, "format": incidentDateFormat})
    else:
        column_settings.append({"header": header})

# Add the table.
uat_worksheet.add_table(
    1, 0, uat_max_row + 1, uat_max_col - 1, {"columns": column_settings}
)

# Make the columns wider for clarity.
uat_worksheet.set_column(0, uat_max_col - 1, 20)

# Close the Pandas Excel writer and output the Excel file.
writer.close()

# order the records in the search result with JQL
