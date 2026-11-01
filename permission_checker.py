import os	#للتعامل مع نظام الملفات (walk,lstat,path)
import stat	#لثوابت الصلاحيات (S_IWOTH, S_ISUID)

def scan(path):	# الدالة المسؤولة عن فحص المجلد المحدد مع جميع المجلدات الفرعية بداخلة
	print(f"[*] Chack : {path}\n")	# تطبع المسار الذي ادخلة المستخدم و الذي سيتم فحصة
	dir_count = 0	# عداد لعدد المجلدات التي تم فحصها
	file_count =0	#عداد لعدد الملفات التي تم فحصها 	
	warning_count =0	# عداد لعدد الملفات التي تم التحذير منها
	for root , dirs , files in os.walk(path , followlinks = False):
 # الدوارة المسؤولة عن المرور على جميع المجلدات
		dir_count+=1 # زيادة عداد المجلدات مع كل مجلد يتم فحصة
		for name in files: # الدوارة المسؤولة عن المرور على جميع الملفات
			file_count +=1 # زيادة عداد الملفات مع كل ملف يتم فحصة
			full = os.path.join(root,name) # دمج اسم الملف مع مسار المجلد
			try:
				mode = os.lstat(full).st_mode # الحصول على نوع المود
			except OSError: # التجاوز اذا كان الملف محمي
				pass
			if mode & stat.S_IWOTH : # اذا تطابق المود مع السماح بالكتابة للجمية يطبع تنبية 
				print(f"[!] allow writing for all : {full}")
				warning_count+=1 # زيادة عداد التنبيهات مع كل تنبية
			if mode & stat.S_ISUID: # اذا تطابق المود مع تنفيذ بصلاحية المالك يطبع تنبية
				print("[!] risk of escalation  : {full}")
				warning_count+=1
	print(f"\n[+] {dir_count} dirs and {file_count} files were checked ")
	# طباعة عدد المجلدات و الملفات التي تم فحصها
	print(f"\n [!!!] Number of Warnings : {warning_count}")
	# طباعة عدد التنبيهات

def main():
	while True: # دوارة للاستمرار في استقبال المسار من المستخدم حتى يدخل مسار صحيح
		try :
			path = input("Enter The Path that you want to scan :")
			#استقبال المسار من المستخدم
			if not os.path.exists(path):
				raise ValueError ( "Path Doesn`t Exist!!" )
				# اذا لم يجد المسار يسبب خطاء  ValueError
			scan(path) #تمرير المسار اذا كان صحيح
			break # التوقف عن استقبال المسار من المستخدم
		except KeyboardInterrupt :
			pass # اذا تم ادخال  ctrl + c  يقوم بالخروج دون اظهار رسالة خطاء
		except ValueError :
			print("Invalid path !!!")
			# اذا كان المسار خاطئ يتم اخبار المستخدم بذالك
			pass
	
if __name__=="__main__": # يقوم بتشغيل دالة المين فقط عندما يتم تشغيل الاسكربت كاكل وليس عند استدعاء مكتبة اسكان فقط
	main()
