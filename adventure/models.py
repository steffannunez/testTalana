import array
from genericpath import exists
from multiprocessing.dummy import Array
from django.db import models

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers
    
    def can_stop(self) -> bool:
        return self.vehicle_type.max_capacity < self.passengers
    
    def get_distribution(self) -> array:
        #se obtiene la maxima capacidad del vehiculo
        #se genera una matriz por defecto 
        mc=self.vehicle_type.max_capacity
        rowModel=[False, False]
        cantRow=0
        matrix=[]
        while cantRow < mc/2:
            matrix.append(rowModel.copy())
            cantRow = cantRow+1
        
        passager = 0
        row = 0
        col = 0 
        while row < len(matrix):
            while col < 2:
                if ((not matrix[row][col]) and passager < mc-1):
                    matrix[row][col] = True
                    passager = passager + 1
                if (passager == mc):
                    return matrix
                col = col +1
            row = row + 1
            col = 0
        if passager < mc:
            return matrix
        return matrix
    def validate_number_plate(plate:str)->bool:
        #metodo a lo bestia jaja
        #revisa todos los valores y verifica que los valores sean numericos donde deben 
        #verifica los guiones y que los primeros dos caracteres no sean letras 
        '''AA-12-34'''
        try :
            alpha1=plate[0].isalpha()
            alpha2=plate[1].isalpha()
            guion1=plate[2]=="-"
            digit1=plate[3].isdigit()
            digit2=plate[4].isdigit()
            guion2=plate[5]=="-"            
            digit3=plate[6].isdigit()
            digit4=plate[7].isdigit()
            if ( alpha1 and alpha2 and guion1 and guion2 and digit1 and digit2 and digit3 and digit4):
                return True
            else:
                return False
        except :
            return False


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self):
        #metodo para saber si un journey ha finalizado 
        #si self.end tiene un largo -es decir- no es nulo, entonces el viaje si termino -True
        #caso contrario retorna False --el viaje no ha terminado
        try :
            if len(self.end) > 0:
                return True
            else:
                return False
        except:
            return False
            