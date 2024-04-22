import threading

# class EXECUTE():
#     def vai(self):
#         print('vai')

#     def vem(self):
#         print('vem')



# exec = EXECUTE()

# def th1(exec: EXECUTE, op: bool):
#     while 1:
#         if op:
#             exec.vai()


# def th2(exec: EXECUTE, op: bool):
#     while 1:
#         if not op:
#             exec.vem()



# thread_1 = threading.Thread(target=th1, args=[exec, True])
# thread_2 = threading.Thread(target=th2, args=[exec, False])


# thread_1.start()
# thread_2.start()

# thread_1.join()
# thread_2.join(),



from cryptography.fernet import Fernet
import base64

chave = b"ola Mundo!ashdiahsodahdosahodpso"
cipher = Fernet(base64.urlsafe_b64encode(chave)) # Para Criptografia Simétrica (AES)