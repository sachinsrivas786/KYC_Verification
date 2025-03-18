from django.db import models

# Create your models here.
class HR_TABLE(models.Model):
    name = models.CharField(max_length=20)
    employee_id = models.IntegerField()

    def __str__(self):
        return '__all__'


class Division(models.Model):
    divisionalid = models.AutoField(primary_key=True)  
    Divisionname = models.CharField(max_length=255) 
    zoneID = models.IntegerField() 

    class Meta:
        db_table = "Division"
        managed = False 
    

class RegionMaster(models.Model):
    regionid = models.AutoField(primary_key=True) 
    regionname = models.CharField(max_length=255) 
    divisionalid = models.ForeignKey(Division, on_delete=models.CASCADE,db_column='divisionalid')  
    state = models.CharField(max_length=255)  

    class Meta:
        db_table = "regionmaster"
        managed = False
        
class UnitMaster(models.Model):
    unitid = models.AutoField(primary_key=True) 
    unitname = models.CharField(max_length=255)  
    districtid = models.IntegerField(null=True, blank=True)
    regionid = models.IntegerField(null=True, blank=True)
    stateid = models.IntegerField(null=True, blank=True)
    esiapplicable = models.BooleanField(default=False)  
    statename = models.CharField(max_length=255, null=True, blank=True)
    isopen = models.BooleanField(default=False) 
    currentaddress = models.TextField(null=True, blank=True)
    workingstatus = models.BooleanField(default=True)  
    dateofopening = models.DateField(null=True, blank=True)
    applicability = models.CharField(max_length=255, null=True, blank=True)
    registrationno = models.CharField(max_length=255, null=True, blank=True)
    renewaldate = models.DateField(null=True, blank=True)
    expirydate = models.DateField(null=True, blank=True)
    docstatus = models.CharField(max_length=255, null=True, blank=True)
    filelink = models.URLField(null=True, blank=True)  
    cmbdocumenttype = models.CharField(max_length=255, null=True, blank=True)
    portfolio_unit_id = models.IntegerField(null=True, blank=True)
    hubid = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    officetypeid = models.IntegerField(null=True, blank=True)
    reportingunitid = models.IntegerField(null=True, blank=True)
    misname = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'unitmaster'  
        managed = False  
        
        


class SonataUsersKYCData(models.Model):
    EmpID = models.CharField(max_length=50, unique=True)
    MobileNo = models.CharField(max_length=15)
    AdhaarNo = models.CharField(max_length=12)
    PAN_Number = models.CharField(max_length=10)
    AdhaarFrontImg = models.BinaryField(null=True, blank=True)
    AdhaarBackImg = models.BinaryField(null=True, blank=True)
    PAN_Img = models.BinaryField(null=True, blank=True)
    RecievedDate = models.DateTimeField(auto_now_add=True)
    IsActive = models.BooleanField(default=True)
    IsProcessed = models.BooleanField(default=False)

    class Meta:
        db_table = "Tbl_Sonata_Users_KYC_Data"
        managed = False 
        
    def __str__(self):
        return self.EmpID
    
class EmployeeMaster(models.Model):
    UnitID = models.IntegerField(null=True, blank=True)
    employee_id = models.IntegerField(primary_key=True)
    EmpDOB = models.DateField(null=True, blank=True)
    StaffTypeID= models.IntegerField(null=True, blank=True)
    DesigID = models.IntegerField(null=True, blank=True)
    DeptID = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    DOR = models.DateField(null=True, blank=True)
    DOJ = models.DateField(null=True, blank=True)
    

    class Meta:
        db_table = 'EmployeeMaster'

    def __str__(self):
        return f"{self.first_name} {self.surname}"
