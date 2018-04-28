import math

class Expression:
    def __init__(self, variable, s_inpt):
        self.var = variable.upper()
        self.s_inpt = s_inpt.upper()
        self.s_inpt = self.s_inpt.replace(' ', '')
        self.first_terms = []
        self.final_terms = []

        self.__convert_to_list()
        self.__create_terms()
        
    def __convert_to_list(self):
        temp_term = ['', '']
        place = 0
        exp = False
        
        for char in self.s_inpt:
            if char in ['+', '-']:
                if not exp:
                    self.first_terms.append(temp_term)
                    temp_term = [char, '']
                    place = 0

                else:
                    temp_term[place] += char
                    exp = False

            elif char == '^':
                exp = True
                temp_term[place] = ''
                
            elif char == self.var:
                place = 1
                temp_term[place] = '1'

            else:
                temp_term[place] += char
                
                if exp:
                    exp = False

        self.first_terms.append(temp_term)

        for term in self.first_terms:
            if term[0] in ['+', '-', '']:
                term[0] = 1

            if term[1] == '':
                term[1] = '0'
                
    def __create_terms(self):
        for term in self.first_terms:
            self.final_terms.append(Term(self, float(term[0]), float(term[1])))
            
    def differentiate(self):
        for term in self.final_terms:
            term.differentiate()
            
    def integrate(self):
        for term in self.final_terms:
            term.integrate()
            
    def calculate(self, value):
        answer = 0
        for term in self.final_terms:
            ans = term.calculate(value)
            if ans == 'u':
                 return 'Undefined'

            else:
                 answer += ans

        return answer
    
    def solve(self, inpt, answer):
        self.final_terms.append(Term(self, answer - self.calculate(inpt), 0))       

    def convert_to_string(self):
        final_text = ''

        for term in self.final_terms:
            final_text += term.convert_to_string()

        if final_text[3:5] == '1' + self.var.lower():
            return final_text[4:]

        else:
            return final_text[3:]


class Term:

    def __init__(self, master, coefficient, exponent):
        self.master = master
        self.coefficient = coefficient
        self.exponent = exponent

    def differentiate(self):
        self.coefficient = self.coefficient * self.exponent
        self.exponent -= 1
       
    def integrate(self):
        if self.exponent == -1:
            self.exponent = 'ln'

        else:
            self.exponent += 1
            self.coefficient = self.coefficient / self.exponent            

    def calculate(self, value):
        try:
            if self.exponent == 'ln':
                return self.coefficient * math.log1p(value - 1)
                
            else:
                return self.coefficient * (value ** self.exponent)

        except:
            return 'u'
        
    def convert_to_string(self):
        temp = ''
        co = self.coefficient
        exp = self.exponent
        
        if co >= 0:
            co = ' + ' + str(co)

        else:
            co = ' - ' + str(co)[1:]

        if exp == 0:
            return co

        elif exp == 1:
            return co + str(self.master.var.lower())

        elif co == 0:
            return ''

        else:
            return co + str(self.master.var.lower()) + '^' + str(exp)

        

        
