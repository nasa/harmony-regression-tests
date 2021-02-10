def write_filetype_test(filename, collection, product_filetype, expected):

    file = open(filename, "w")
    file.write("import pytest\n")
    file.write("def test_" + collection + "_" + expected['q_num'] +"_filetype():\n")
    file.write("    assert "+"'"+product_filetype+"'"+" == "+"'"+expected['file_type']+"'"+"\n")
    file.close()
    return
