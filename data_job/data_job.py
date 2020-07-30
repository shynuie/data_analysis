import pandas as pd


def tf_salary(og_data):
    og_data["Salary Estimate"] = og_data["Salary Estimate"].str.replace("-1","0-0")
    og_data["Salary Estimate"] = og_data["Salary Estimate"].str.replace("$","")
    og_data["Salary Estimate"] = og_data["Salary Estimate"].str.split("(").str[0]
    # og_data["Salary Estimate"] = og_data["Salary Estimate"].str.replace(r"\(\w*\s*\w*\.\)","")   #regular expreesing also works
    og_data["Salary Estimate"] = og_data["Salary Estimate"].str.replace("K","000").str.strip()
    og_data["Salary_Min"] = og_data["Salary Estimate"].str.split("-").str[0]
    og_data["Salary_Max"] = og_data["Salary Estimate"].str.split("-").str[1]
    og_data["Salary_Min"] = og_data["Salary_Min"].astype("int")
    og_data["Salary_Max"] = og_data["Salary_Max"].astype("int")
    return og_data


def tf_size(og_data):
    og_data["Size"] = og_data["Size"].str.replace("Unknown", "-1")
    og_data["Size"] = og_data["Size"].str.replace(r"\w*\s+to", "")
    og_data["Size"] = og_data["Size"].str.replace("employees", "")
    og_data["Size"] = og_data["Size"].str.replace(r"10000\+", "10001").str.strip()
    return og_data


def tf_revenue(og_data):
    og_data["Revenue"] = og_data["Revenue"].str.replace("Unknown / Non-Applicable", "0 to $0")
    og_data["Revenue"] = og_data["Revenue"].str.replace("500 million", "0.5")
    og_data["Revenue"] = og_data["Revenue"].str.replace(r"Less\s+than\s+\$1\s+million", "1 to $100 million")
    og_data["Revenue"] = og_data["Revenue"].str.replace(r"\+", " to $100")
    og_data["Revenue"] = og_data["Revenue"].str.replace(r"\(USD\)", "")
    og_data["Revenue_min"] = og_data["Revenue"].str.split(r"to\s\$").str[0].fillna(0)
    og_data["Revenue_min"] = og_data["Revenue_min"].str.replace(r"\$","").str.strip().fillna(0)
    og_data["Revenue_back"] = og_data["Revenue"].str.split(r"to\s\$").str[1].fillna(0)
    og_data["Revenue_max"] = og_data["Revenue_back"].str.split(" ").str[0].fillna(0)
    og_data["Revenue_unit"] = og_data["Revenue_back"].str.split(" ").str[1]
    og_data["Revenue_unit"] = og_data["Revenue_unit"].str.replace("billion", "1000000000").str.strip(r"\s")
    og_data["Revenue_unit"] = og_data["Revenue_unit"].str.replace("million", "1000000").str.strip().fillna(1).replace("","1")
    og_data["Revenue_min"] = og_data["Revenue_min"].astype("float")
    og_data["Revenue_max"] = og_data["Revenue_max"].astype("float")
    og_data["Revenue_unit"] = og_data["Revenue_unit"].astype("int")
    og_data["Revenue_min"] = og_data["Revenue_min"] * og_data["Revenue_unit"]
    og_data["Revenue_max"] = og_data["Revenue_max"] * og_data["Revenue_unit"]
    og_data = og_data.drop(["Revenue_back", "Revenue_unit"], axis = 1)
    return og_data


def tf_apply(og_data):
    og_data["Easy Apply"] = og_data["Easy Apply"].str.replace("-1", "0")
    og_data["Easy Apply"] = og_data["Easy Apply"].str.replace(r"[^0]", "1")
    og_data["Easy Apply"] = og_data["Easy Apply"].astype("int").astype("bool")
    return og_data


def tf_company(og_data):
    og_data["Company Name"] = og_data["Company Name"].str.split("\n").str[0]
    return og_data


def transform(data):
    data = tf_salary(data)
    data = tf_size(data)
    data = tf_revenue(data)
    data = tf_apply(data)
    data = tf_company(data)
    tf_data = data[["Company Name", "Job Title", "Salary_Min","Salary_Max", "Size", "Rating", "Revenue_min", "Revenue_max", "Job Description", "Location", "Founded", "Type of ownership", "Industry", "Sector", "Headquarters", "Easy Apply" ]]
    return tf_data


def year_ratio(years):
    if years > 8:
        return 1
    else:
        return years ** 2 / 8 ** 2


def predicted_salary(data, yr):
    data["Predicted_Salary"] = (data["Salary_Max"]-data["Salary_Min"]) * yr + data["Salary_Min"]
    return data


def find_high_salary(data):
    work_years = float(input("Pls enter your relevent working years:"))
    yr = year_ratio(work_years)
    data = predicted_salary(data, yr)
    print(data.sort_values(by = ["Predicted_Salary", "Rating"] , ascending = [False, False]).head(25))




og_data = pd.read_csv("/Users/Marvin/Desktop/D_A/data_job/DataAnalyst.csv", index_col=0)
tf_data = transform(og_data)
find_high_salary(tf_data)
