#from flyquery import flyquery as flyq
import pygsheets

gc = pygsheets.authorize()
# Open spreadsheet and then workseet
#sh = gc.open('Stocks Ricardo.xls')
#wks = sh.sheet1
#df = wks.get_as_df()
# Update a cell with value (just to let him know values is updated ;) )
#wks.update_cell('A1', "Hey yank this numpy array")

# update the sheet with array
#wks.update_cells('A2', my_nparray.to_list())

# share the sheet with your friend
#sh.share("myFriend@gmail.com")
