 create DATABASE if not exists ICSI_Cleaned_Data;
 use ICSI_Cleaned_Data;
 CREATE TABLE ICSI_Cleaned_Data (
    Record_ID VARCHAR(50),
    Selection_Date DATE,
    Patient_ID VARCHAR(50),
    Cycle_Number INT,
    Oocyte_ID VARCHAR(50),
    Embryologist_ID VARCHAR(50),
    Embryologist_Experience_Years INT,

    Sperm_Concentration_M_per_ml DECIMAL(6,2),
    Total_Motility_Percent DECIMAL(5,2),
    Progressive_Motility_Percent DECIMAL(5,2),
    Normal_Morphology_Percent DECIMAL(5,2),

    Selection_Time_Seconds INT,
    Head_Shape_Score DECIMAL(4,2),
    Acrosome_Status VARCHAR(20),
    Midpiece_Assessment VARCHAR(20),
    Tail_Assessment VARCHAR(20),
    Motility_Pattern VARCHAR(20),
    Vacuoles_Present VARCHAR(10),

    Fertilization_Success VARCHAR(10),
    Day3_Grade VARCHAR(20),
    Day5_Blastocyst_Grade VARCHAR(20),
    Usable_Embryo VARCHAR(10),

    Microscope_Type VARCHAR(50),
    Magnification_Used INT,
    Lab_Temperature_C DECIMAL(4,2),
    Lab_Humidity_Percent DECIMAL(5,2)
);
show tables;

SELECT COUNT(*) AS total_records
FROM icsi_cleaned_data;

DESCRIBE icsi_cleaned_data;

# find null----------------
SELECT
    SUM(Embryologist_Experience_Years IS NULL) AS exp_nulls,
    SUM(Sperm_Concentration_M_per_ml IS NULL) AS sperm_nulls,
    SUM(Total_Motility_Percent IS NULL) AS motility_nulls,
    SUM(Normal_Morphology_Percent IS NULL) AS morphology_nulls,
    SUM(Lab_Temperature_C IS NULL) AS temp_nulls,
    SUM(Lab_Humidity_Percent IS NULL) AS humidity_nulls
FROM icsi_cleaned_data;

# Record_id----------------
SELECT Record_ID, COUNT(*) AS cnt
FROM icsi_cleaned_data
GROUP BY Record_ID
HAVING COUNT(*) > 1;

#finding min, avg, max , std_sperm-------------
SELECT
    MIN(Sperm_Concentration_M_per_ml) AS min_sperm,
    MAX(Sperm_Concentration_M_per_ml) AS max_sperm,
    ROUND(AVG(Sperm_Concentration_M_per_ml),2) AS avg_sperm,
    ROUND(STDDEV(Sperm_Concentration_M_per_ml),2) AS std_sperm
FROM icsi_cleaned_data;


select distinct Fertilization_Success
from icsi_cleaned_data;
# Success count---------------
select distinct Fertilization_Success
from icsi_cleaned_data;
SELECT Fertilization_Success, COUNT(*) AS count
FROM icsi_cleaned_data
GROUP BY Fertilization_Success;
# Usable_embryo count------------
SELECT Usable_Embryo, COUNT(*) AS count
FROM icsi_cleaned_data
GROUP BY Usable_Embryo;

# temperatuer and humidity --------
SELECT
    MIN(Lab_Temperature_C) AS min_temp,
    MAX(Lab_Temperature_C) AS max_temp,
    ROUND(AVG(Lab_Temperature_C),2) AS avg_temp,
    ROUND(AVG(Lab_Humidity_Percent),2) AS avg_humidity
FROM icsi_cleaned_data;

# average sperm , average motility , average morphology by  fertilitiy success
SELECT
    Fertilization_Success,
    ROUND(AVG(Sperm_Concentration_M_per_ml),2) AS avg_sperm,
    ROUND(AVG(Total_Motility_Percent),2) AS avg_motility,
    ROUND(AVG(Normal_Morphology_Percent),2) AS avg_morphology
FROM icsi_cleaned_data
GROUP BY Fertilization_Success;

# average experience and fertilization success-------------
SELECT
    Fertilization_Success,
    ROUND(AVG(Embryologist_Experience_Years),2) AS avg_experience
FROM icsi_cleaned_data
GROUP BY Fertilization_Success;

# day5 blastocyst grade----------
SELECT
    Day5_Blastocyst_Grade,
    COUNT(*) AS count
FROM icsi_cleaned_data
GROUP BY Day5_Blastocyst_Grade
order by count asc;




