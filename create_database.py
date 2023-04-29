import mysql.connector
from mysql.connector import errorcode
# # Database object

#establish a connection with  MySQL server 
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="PixelDcs_Dc0"
)
mycursor = cnx.cursor()
mycursor.execute("DROP DATABASE SQC")
mycursor.execute("CREATE DATABASE IF NOT EXISTS SQC")
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="PixelDcs_Dc0",
    database="SQC"
)
mycursor = mydb.cursor()

class SQLDataBase(): 
    def __init__(self): 
        self.create_tables()
        self.insert_data_analyzer()
        self.insert_data_test()
        self.insert_data_reagents()
        self.insert_data_qc_parameters()
        self.insert_data_qc_results()
        self.insert_data_test_analyzer()
        self.insert_data_calculated_parameters()
        self.insert_data_lab() 
      
    def create_tables(self):   
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS Analyzer (analyzer_id INT NOT NULL, analyzer_name VARCHAR(255), anlyzer_manufacturer VARCHAR(255), analyzer_model VARCHAR(255), PRIMARY KEY(analyzer_id))")
        
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS Test (test_code INT NOT NULL, test_name VARCHAR(255), test_measurement_unit VARCHAR(255), test_delta_check VARCHAR(255), test_analytical_quality_goal VARCHAR(255), test_group VARCHAR(255), PRIMARY KEY(test_code))")
        
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS Reagents (reagent_lot_number INT NOT NULL, reagent_name VARCHAR(255), reagent_manufacturer VARCHAR(255), reagent_expiry_date DATE, PRIMARY KEY(reagent_lot_number))")
        
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS test_analyzer (a_id INT NOT NULL, t_code INT NOT NULL, r_lot_number INT NOT NULL, linear_range_from INT, linear_range_to INT, FOREIGN KEY (a_id) REFERENCES Analyzer(analyzer_id), FOREIGN KEY (t_code) REFERENCES Test(test_code), FOREIGN KEY (r_lot_number) REFERENCES Reagents(reagent_lot_number))")
        
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS QC_Parameters (qc_id INT NOT NULL, qc_lot_number INT NOT NULL, qc_name VARCHAR(255), qc_type VARCHAR(255), qc_level VARCHAR(255), qc_manufacturer VARCHAR(255), qc_speciality VARCHAR(255), qc_expiry_date DATE, PRIMARY KEY(qc_id))")
        
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS test_qc_results (t_code INT NOT NULL, a_id INT NOT NULL, r_lot_number INT NOT NULL, q_c_id INT NOT NULL, qc_assigned_mean INT, qc_assigned_sd INT, qc_assigned_cv INT, qualitative_assigned INT, qc_result INT, qc_flag BOOLEAN, qc_date DATE, qc_calculated_mean INT, qc_calculated_sd INT, qc_calculated_cv INT, qc_overall_status VARCHAR(255), FOREIGN KEY (t_code) REFERENCES Test(test_code), FOREIGN KEY (a_id) REFERENCES Analyzer(analyzer_id), FOREIGN KEY (r_lot_number) REFERENCES Reagents(reagent_lot_number), FOREIGN KEY (q_c_id) REFERENCES QC_Parameters(qc_id))")
        
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS Calculated_Parameters (ids INT NOT NULL, no_of_points INT, mu INT, ewma INT, cusum INT, PRIMARY KEY(ids))")
        
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS patch_panels (lab_id INT NOT NULL, a_id INT NOT NULL, patch_panel VARCHAR(255), hw_unit VARCHAR(255), PRIMARY KEY(lab_id), FOREIGN KEY (a_id) REFERENCES Analyzer(analyzer_id))")
        
        mycursor.execute("SHOW TABLES")
        for x in mycursor:
            print(x)
    
    
    def insert_data_analyzer(self): 
        sql = "INSERT INTO Analyzer (analyzer_id, analyzer_name, anlyzer_manufacturer, analyzer_model) VALUES (%s, %s, %s, %s)"
        val = [
        ('1001', 'Analyzer1', 'Company1', 'M1'),
        ('1002', 'Analyzer2', 'Company1', 'M2'),
        ('1003', 'Analyzer3', 'Company1', 'M3'),
        ('1004', 'Analyzer1', 'Company2', 'M4'),
        ('1005', 'Analyzer2', 'Company2', 'M5'),
        ('1006', 'Analyzer3', 'Company2', 'M6'),
        ('1007', 'Analyzer1', 'Company3', 'M7'),
        ('1008', 'Analyzer2', 'Company3', 'M8'),
        ('1009', 'Analyzer3', 'Company3', 'M9'),
        ('1010', 'Analyzer1', 'Company4', 'M10'),
        ('1011', 'Analyzer2', 'Company4', 'M11'),
        ('1012', 'Analyzer2', 'Company4', 'M12'),
        ('1013', 'Analyzer3', 'Company5', 'M13'),
        ('1014', 'Analyzer1', 'Company5', 'M14'),
        ('1015', 'Analyzer2', 'Company5', 'M15'),
        ('1016', 'Analyzer3', 'Company6', 'M16'),
        ]
        
        mycursor.executemany(sql, val)
        mydb.commit()
    
    
    # class SQLDataBase(self): 
    #     def __init__(self):        
    #         pass
    def insert_data_test(self): 
        sql = "INSERT INTO Test (test_code, test_name, test_measurement_unit, test_delta_check, test_analytical_quality_goal, test_group) VALUES (%s, %s,%s, %s, %s, %s)"
        val = [
        ('2001', 'Glucose', 'mg/dL', 'Function1', 'Goal1', 'Group1'),
        ('2002', 'Acetaminophen', 'mg/mL', 'Function2', 'Goal2', 'Group2'),
        ('2003', 'Albumin', 'g/dL', 'Function3', 'Goal3', 'Group3'),
        ('2004', 'Cholesterol', 'mg/dL', 'Function4', 'Goal4', 'Group4'),
        ('2005', 'Glucose', 'mg/dL', 'Function5', 'Goal5', 'Group5'),
        ('2006', 'Acetaminophen', 'mg/mL', 'Function6', 'Goal6', 'Group6'),
        ('2007', 'Albumin', 'g/dL', 'Function7', 'Goal7', 'Group7'),
        ('2008', 'Cholesterol', 'mg/dL', 'Function8', 'Goal8', 'Group8'),
        ('2009', 'Glucose', 'mg/dL', 'Function9', 'Goal9', 'Group9'),
        ('2010', 'Acetaminophen', 'mg/mL', 'Function10', 'Goal10', 'Group10'),
        ('2011', 'Albumin', 'g/dL1', 'Function11', 'Goal11', 'Group11'),
        ('2012', 'Cholesterol', 'mg/dL2', 'Function12', 'Goal12', 'Group12'),
        ('2013', 'Glucose', 'mg/dL', 'Function13', 'Goal13', 'Group13'),
        ('2014', 'Acetaminophen', 'mg/mL', 'Function14', 'Goal14', 'Group14'),
        ('2015', 'Albumin', 'g/dL', 'Function15', 'Goal15', 'Group15'),
        ('2016', 'Cholesterol', 'mg/dL', 'Function16', 'Goal16', 'Group16'),
        ]
        
        mycursor.executemany(sql, val)
        mydb.commit()
    
    def insert_data_reagents(self): 
        sql = "INSERT INTO Reagents (reagent_lot_number, reagent_name, reagent_manufacturer, reagent_expiry_date) VALUES (%s, %s, %s, %s)"
        val = [
        ('3001', 'Reagent1', 'M1', '2021-1-1'),
        ('3002', 'Reagent2', 'M2', '2021-2-26'),
        ('3003', 'Reagent3', 'M3', '2021-3-30'),
        ('3004', 'Reagent4', 'M4', '2021-4-4'),
        ('3005', 'Reagent5', 'M5', '2021-5-5'),
        ('3006', 'Reagent6', 'M6', '2021-6-6'),
        ('3007', 'Reagent7', 'M7', '2021-7-17'),
        ('3008', 'Reagent8', 'M8', '2021-8-8'),
        ('3009', 'Reagent9', 'M9', '2021-9-9'),
        ('3010', 'Reagent10', 'M10', '2021-10-10'),
        ('3011', 'Reagent11', 'M9', '2021-10-6'),
        ('3012', 'Reagent12', 'M9', '2021-11-16'),
        ('3013', 'Reagent13', 'M11', '2021-12-28'),
        ('3014', 'Reagent14', 'M12', '2021-11-13'),
        ('3015', 'Reagent15', 'M13', '2021-10-21'),
        ('3016', 'Reagent16', 'M13', '2021-12-12'),
        
        ]
        mycursor.executemany(sql, val)
        mydb.commit()
    
    def insert_data_qc_parameters(self): 
        sql = "INSERT INTO QC_Parameters (qc_id, qc_lot_number, qc_name, qc_type, qc_level, qc_manufacturer,qc_speciality, qc_expiry_date) VALUES (%s, %s,%s, %s, %s, %s, %s, %s)"
        val = [
        ('4001', '401', 'QC1', 'Type1', 'Level1', 'M1', 'SP1', '2022-1-1'),
        ('4002', '401', 'QC2', 'Type2', 'Level1', 'M2', 'SP2', '2022-1-1'),
        ('4003', '401', 'QC2', 'Type3', 'Level2', 'M3', 'SP3', '2022-2-2'),
        ('4004', '401', 'QC2', 'Type4', 'Level1', 'M4', 'SP4', '2022-2-2'),
        ('4005', '401', 'QC2', 'Type5', 'Level2', 'M5', 'SP5', '2022-3-3'),
        ('4006', '401', 'QC2', 'Type6', 'Level1', 'M6', 'SP6', '2022-3-3'),
        ('4007', '402', 'QC2', 'Type7', 'Level2', 'M7', 'SP7', '2022-4-4'),
        ('4008', '402', 'QC2', 'Type8', 'Level1', 'M8', 'SP8', '2022-4-4'),
        ('4009', '402', 'QC2', 'Type9', 'Level2', 'M9', 'SP9', '2022-5-5'),
        ('4010', '402', 'QC1', 'Type10', 'Level2', 'M10', 'SP10', '2022-5-5'),
        ('4011', '402', 'QC1', 'Type11', 'Level2', 'M11', 'SP11', '2022-6-6'),
        ('4012', '403', 'QC1', 'Type12', 'Level1', 'M12', 'SP12', '2022-6-6'),
        ('4013', '403', 'QC1', 'Type13', 'Level1', 'M13', 'SP13', '2022-7-7'),
        ('4014', '403', 'QC1', 'Type14', 'Level2', 'M14', 'SP14', '2022-7-7'),
        ('4015', '403', 'QC1', 'Type15', 'Level2', 'M15', 'SP15', '2022-8-8'),
        ('4016', '403', 'QC2', 'Type16', 'Level1', 'M16', 'SP16', '2022-8-8'),
        ('4017', '403', 'QC2', 'Type16', 'Level2', 'M16', 'SP16', '2022-8-8'),
        ('4018', '401', 'QC1', 'Type1', 'Level2', 'M1', 'SP1', '2022-1-1'),
        
        ]
        
        mycursor .executemany(sql, val)
        mydb.commit()
    
    def insert_data_qc_results(self): 
        sql = "INSERT INTO test_qc_results (t_code, a_id, r_lot_number, q_c_id, qc_assigned_mean, qc_assigned_sd, qc_assigned_cv, qualitative_assigned, qc_result, qc_flag, qc_date, qc_calculated_mean, qc_calculated_sd, qc_calculated_cv, qc_overall_status) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"
        val = [
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '93', '1', '2021-9-1', '95', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '88', '1', '2021-9-2', '90', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '101', '1', '2021-9-3', '93', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '87', '1', '2021-9-4', '92', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '81', '1', '2021-9-5', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '82', '1', '2021-9-6', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '83', '1', '2021-9-7', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '84', '1', '2021-9-8', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '84', '1', '2021-9-9', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '83', '1', '2021-9-10', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '82', '1', '2021-9-11', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '95', '1', '2021-9-12', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '81', '1', '2021-9-13', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '110', '1', '2021-9-14', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '86', '1', '2021-9-15', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '103', '1', '2021-9-16', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '101', '1', '2021-9-17', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '102', '1', '2021-9-18', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4001', '90', '5', '15', '17', '103', '1', '2021-9-19', '91', '9', '19', 'PENDING'),
        
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '89', '1', '2021-9-1', '95', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '88', '1', '2021-9-2', '90', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '95', '1', '2021-9-3', '93', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '96', '1', '2021-9-4', '93', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '96', '1', '2021-9-5', '93', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '97', '1', '2021-9-6', '93', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '98', '1', '2021-9-7', '93', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '87', '1', '2021-9-8', '92', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '82', '1', '2021-9-9', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '78', '1', '2021-9-10', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '79', '1', '2021-9-11', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '75', '1', '2021-9-12', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '95', '1', '2021-9-13', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '82', '1', '2021-9-14', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '95', '1', '2021-9-15', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '86', '1', '2021-9-16', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '94', '1', '2021-9-17', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '94', '1', '2021-9-18', '91', '9', '19', 'PENDING'),
        ('2001', '1001', '3001', '4018', '90', '5', '15', '17', '94', '1', '2021-9-19', '91', '9', '19', 'PENDING'),
        
        ('2016', '1016', '3003', '4016', '70', '6', '80', '70', '78', '1', '2021-8-18', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4016', '70', '6', '80', '70', '78', '1', '2021-8-19', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4016', '70', '6', '80', '70', '78', '1', '2021-8-20', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4016', '70', '6', '80', '70', '78', '1', '2021-8-21', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4016', '70', '6', '80', '70', '75', '1', '2021-8-22', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4016', '70', '6', '80', '70', '65', '1', '2021-8-23', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4016', '70', '6', '80', '70', '61', '1', '2021-8-24', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4016', '70', '6', '80', '70', '61', '1', '2021-8-25', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4016', '70', '6', '80', '70', '61', '1', '2021-8-27', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4016', '70', '6', '80', '70', '61', '1', '2021-8-28', '75', '19', '70', 'COMPLETE'),
        
        ('2016', '1016', '3003', '4017', '70', '6', '80', '70', '88', '1', '2021-8-18', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4017', '70', '6', '80', '70', '87', '1', '2021-8-19', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4017', '70', '6', '80', '70', '85', '1', '2021-8-20', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4017', '70', '6', '80', '70', '89', '1', '2021-8-21', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4017', '70', '6', '80', '70', '75', '1', '2021-8-22', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4017', '70', '6', '80', '70', '64', '1', '2021-8-23', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4017', '70', '6', '80', '70', '65', '1', '2021-8-24', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4017', '70', '6', '80', '70', '58', '1', '2021-8-25', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4017', '70', '6', '80', '70', '72', '1', '2021-8-27', '75', '19', '70', 'COMPLETE'),
        ('2016', '1016', '3003', '4017', '70', '6', '80', '70', '71', '1', '2021-8-28', '75', '19', '70', 'COMPLETE'),
        
        # ('2004', '1004', '3004', '4004', '90',  '5',   '19',  '50',  '87', '0',     '2021-2-4', '54', '45', '20', 'COMPLETE'),
        # ('2005', '1005', '3005', '4005', '70',  '6',   '40',  '50',  '63', '1',      '2021-3-5', '95', '40', '20', 'COMPLETE'),
        # ('2006', '1006', '3006', '4006', '90',  '5',   '80',  '48',  '89', '1',      '2021-3-26', '35', '91', '89', 'COMPLETE'),
        # ('2007', '1007', '3007', '4007', '70',  '6',   '19',  '38',  '68', '0',     '2021-4-7', '95', '30', '20', 'PENDING'),
        # ('2008', '1008', '3008', '4008', '90',  '5',   '20',  '99',  '97', '1',       '2021-5-8', '80', '15', '19', 'PENDING'),
        # ('2009', '1009', '3009', '4009', '70',  '6',   '92',  '18',  '96', '1',       '2021-6-9', '30', '80', '80', 'COMPLETE'),
        # ('2010', '1010', '3010', '4010', '70',  '6',   '26',  '138', '78','1',    '2021-7-10', '50', '90', '100', 'COMPLETE'),
        # ('2011', '1011', '3011', '4011', '70',  '6',   '150', '90',  '92','1',    '2021-8-8', '90', '100', '145', 'PENDING'),
        # ('2012', '1012', '3012', '4012', '90',  '5',   '70',  '28',  '88','1',       '2021-9-18', '20', '26', '78', 'PENDING'),
        # ('2013', '1013', '3013', '4013', '90',  '5',   '18',  '28',  '92','1',       '2021-9-29', '90', '70', '15', 'PENDING'),
        # ('2014', '1014', '3014', '4014', '70',  '6',   '150', '82',  '58','0',  '2021-10-15', '95', '107', '152', 'PENDING'),
        # ('2015', '1015', '3015', '4015', '70',  '6',   '61',  '21',  '70','1',       '2021-11-20', '75', '90', '60', 'PENDING'),
        # ('2016', '1016', '3016', '4016', '70',  '6',   '29',  '63',  '60','1',     '2021-12-22', '95', '90', '19', 'PENDING'),
        ]
        
        mycursor .executemany(sql, val)
        mydb.commit()
    
    def insert_data_test_analyzer(self): 
        sql = "INSERT INTO test_analyzer (a_id, t_code, r_lot_number, linear_range_from , linear_range_to) VALUES (%s, %s, %s, %s, %s)"
        val = [
        ('1001', '2001', '3001', '10', '20'),
        ('1002', '2002', '3002', '10', '20'),
        ('1003', '2003', '3003', '10', '20'),
        ('1004', '2004', '3004', '10', '20'),
        ('1005', '2005', '3005', '10', '20'),
        ('1006', '2006', '3006', '10', '20'),
        ('1007', '2007', '3007', '10', '20'),
        ('1008', '2008', '3008', '10', '20'),
        ('1009', '2009', '3009', '10', '20'),
        ('1010', '2010', '3010', '10', '20'),
        ('1011', '2011', '3011', '10', '20'),
        ('1012', '2012', '3012', '10', '20'),
        ('1013', '2013', '3013', '10', '20'),
        ('1014', '2014', '3014', '10', '20'),
        ('1015', '2015', '3015', '10', '20'),
        ('1016', '2016', '3016', '10', '20')
        ]
        
        mycursor .executemany(sql, val)
        mydb.commit()
        
    def insert_data_calculated_parameters(self): 
        sql = "INSERT INTO Calculated_Parameters (ids, no_of_points, mu, ewma, cusum) VALUES (%s, %s, %s, %s, %s)"
        val = [
        ('6001', '120', '13', '18','29'),
        ]
        
        mycursor .executemany(sql, val)
        mydb.commit()
    
    def insert_data_lab(self): 
        sql = "INSERT INTO patch_panels (lab_id, a_id, patch_panel, hw_unit) VALUES (%s, %s, %s, %s)"
        val = [
        ('0001', '1001', 'PP0', 'EOS'),  # 1
        ('0002', '1002', 'PP0', 'EOS'),  # 2
        ('0003', '1003', 'PP0', 'EOS'),  # 3
        ('0004', '1004', 'PP0', 'EOS'),  # 1
        ('0005', '1005', 'PP0', 'Opto Boards'),  # 2
        ('0006', '1006', 'PP0', 'Opto Boards'),  # 3
        ('0007', '1007', 'PP1', 'Opto Boards'),  # 1
        ('0008', '1008', 'PP1', 'Opto Boards'),  # 2
        ('0009', '1009', 'PP1', 'Opto Boards'),  # 3
        ('0010', '1010', 'PP1', 'Opto Boards'),  # 1
        ('0011', '1011', 'PP1', 'Opto Boards'),  # 2
        ('0012', '1012', 'PP2', 'Monitoring Card'),  # 2
        ('0013', '1013', 'PP2', 'Opto Boards'),  # 3
        ('0014', '1014', 'PP2', 'Monitoring Card'),  # 1
        ('0015', '1015', 'PP2', 'Monitoring Card'),  # 2
        ('0016', '1016', 'PP2', 'Opto Boards')  # 3
        ]
        mycursor.executemany(sql, val)
        mydb.commit()
    
def main(): 
    database = SQLDataBase()   
              
if __name__ == "__main__":
    main()      