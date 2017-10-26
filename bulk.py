import os


folder = 'json_files'

bulk_counter = 0
write_file = open('json_bulks/bulk' + str(bulk_counter) + '.json', 'w')
for i, file in enumerate(os.listdir(folder)):
	print(i)
	if (i % 25000) == 0:
		if i != 0:
			write_file.close()
			bulk_counter += 1
			write_file = open('json_bulks/bulk' + str(bulk_counter) + '.json', 'w')

	with open(folder + '/' + file, 'r') as text_file:
		for line in text_file:
			write_file.write('{"index" : {"_index": "index", "_type": "document", "_id":\"'+file[:-5]+'\"}}\n')
			write_file.write(line)
			write_file.write('\n')

write_file.close()
print()