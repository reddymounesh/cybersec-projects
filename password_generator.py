import  argparse
import secrets
import random
import string

parser=argparse.ArgumentParser(
    prog='Password Genrator',
    description='Generate any number of passwords with this tool.'
)


parser.add_argument("-n","--numbers",default=0,help="Numbers of digits in the PW",type=int)
parser.add_argument("-l","--lowercase",default=0,help="Numbers of lowercase in the PW",type=int)
parser.add_argument("-u","--uppercase",default=0,help="Numbers of uppercase chars in the PW",type=int)
parser.add_argument("-s","--special_chars",default=0,help="Numbers of special chars in the PW",type=int)

parser.add_argument("-t","--total_length",type=int,help="The total password length ,if passed it will ignore -n,-l,-u and -s ,"\
                    "and generate random passwords with specified length")
parser.add_argument("-a","--amount",default=1,type=int,help="The number of passwords to generate")

parser.add_argument("-o","--output-file",help="file to save generated passwords")


args=parser.parse_args()


passwords=[]

for _ in range(args.amount):
    if args.total_length:
        passwords.append("".join(
            [secrets.choice(string.digits + string.ascii_letters + string.punctuation)  
                for _ in range(args.total_length)]))
        


    else:
        password=[]

        for _ in range(args.numbers):
            password.append(secrets.choice(string.digits))

        for _ in range(args.uppercase):
            password.append(secrets.choice(string.ascii_uppercase))

        for _ in range(args.lowercase):
            password.append(secrets.choice(string.ascii_lowercase))

        for _ in range(args.special_chars):
            password.append(secrets.choice(string.punctuation))


        random.shuffle(password)

        password=''.join(password)

        passwords.append(password)


if args.output_file:
    with open(args.output_file,'w') as f:
        f.write('\n'.join(passwords))

else:
    print('\n'.join(passwords))




