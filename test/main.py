from os import system
cur_file = __file__.replace("\\","/")
prj_directory = "/".join(cur_file.split('/')[:-2])

test_cases = ['authorization_test',
              'users_test',
              'units_test',
              'categories_test',
              'customers_test',
              'products_test',
              'sales_test',
              'purchases_test'] 
        
if __name__ == "__main__":
    for test in test_cases:
        system(f'pytest -v {prj_directory}/test/{test}.py --html={prj_directory}/documentation/{test}_report.html --tb=line') 