import pyodbc
import pandas as pd

class NewSKU():

    global cur,Category,Owner_name,ITEM_ID,BATCH_CODE,DESCRIPTION

    conn = ("""driver={SQL Server};server={{ SQL Port }};database={{ SQL Database}};
        trusted_connection=no;UID={{ SQL UID }};PWD={{ SQL Password }};IntegratedSecurity = true;""")
    conx = pyodbc.connect(conn)
    cur = conx.cursor() 
    
    def reading_csv(self):
            Dataset = pd.read_csv(r'C:\Users\shara\OneDrive\Desktop\test_book.csv',delimiter='\t')
            Dict_data = Dataset.to_dict(orient='records')
            for x in range(len(Dict_data)):
                TABLE_DATA = Dict_data[x]
                # print(TABLE_DATA)
                ITEM_ID = str(TABLE_DATA["ItemId"])              #SKU CODE
                # print(ITEM_ID)
                DESCRIPTION = str(TABLE_DATA["Description"])    #Description of SKU
                # print(DESCRIPTION)
                Category = str(TABLE_DATA["Category"])    #Description of SKU
                # print(Category)
                Owner_name = str(TABLE_DATA["OwnerName"])    #Owner Name 
                # print(Owner_name)
                BATCH_CODE = str(TABLE_DATA["BatchCode"])    #Batch Code of SKU
                # print(BATCH_CODE)
                self.check_Category(Category,Owner_name,ITEM_ID,BATCH_CODE,DESCRIPTION)

    def check_Category(self,Category,Owner_name,ITEM_ID,BATCH_CODE,DESCRIPTION):
        SELECT_QUERY1 = "SELECT OwnerCategoryId FROM OwnerCategories WHERE Name =  '"+Category+"'"
        exe1 = cur.execute(SELECT_QUERY1)
        data = exe1.fetchall()
        # print(data)

        if not data:
            SELECT_QUERY2 = "SELECT OwnerId FROM Owners WHERE Name =  '"+Owner_name+"'"
            exe_O = cur.execute(SELECT_QUERY2)
            data1 = exe_O.fetchall()
            Owner_ID = data1[0][0]
            # print(Owner_ID)

            INSERT_QUERY1 = "INSERT INTO [dbo].[OwnerCategories]([OwnerId],[Name],[SerializedFlag],[LotFlag],[CreatedBy],[CreatedDate])VALUES('"+str(Owner_ID)+"','"+str(Category)+"','N','N','EmizaSupport',GETDATE())"
            # print(INSERT_QUERY)
            exe2 = cur.execute(INSERT_QUERY1)
            print(cur.rowcount, "Category Added")
            cur.commit()

            SELECT_QUERY3 = "SELECT OwnerCategoryId FROM OwnerCategories WHERE Name = '"+Category+"'"
            exe3 = cur.execute(SELECT_QUERY3)
            data3 = exe3.fetchall()
            CategoryID = data3[0][0]
            print(CategoryID)
            self.checkItemID(CategoryID,ITEM_ID,BATCH_CODE,DESCRIPTION)
        else:
            CategoryID = data[0][0]
            print(CategoryID)
            print(Category,",Category is Available")
            self.checkItemID(CategoryID,ITEM_ID,BATCH_CODE,DESCRIPTION)

    def checkItemID(self,CategoryID,ITEM_ID,BATCH_CODE,DESCRIPTION):

        SELECT_QUERY4 = "SELECT ItemId FROM ItemMaster WHERE ItemId ='"+ITEM_ID+"'"
        exe_NO = cur.execute(SELECT_QUERY4)
        data4 = exe_NO.fetchall()

        if not data4:
            INSERT_QUERY2 = "INSERT INTO [dbo].[ItemMaster] ([ItemId],[OwnerCategoryId],[AltItemId1],[Description],[CreatedBy],[CreatedDate],[CFT])VALUES('"+str(ITEM_ID)+"','"+str(CategoryID)+"','"+str(BATCH_CODE)+"','"+str(DESCRIPTION)+"','EmizaSupport',GETDATE(),'1')"
            exe3 = cur.execute(INSERT_QUERY2)
            print(cur.rowcount, "Item_ID Added")
            cur.commit()
            # print(INSERT_QUERY2)
        else:
            Owner_ID = data4[0][0]
            print(Owner_ID,"Item ID Present")
a1 = NewSKU()
a1.reading_csv()