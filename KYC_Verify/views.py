from django.shortcuts import render
import json
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .forms import CandidateForm
from .models import HR_TABLE, Division, EmployeeMaster, RegionMaster, SonataUsersKYCData, UnitMaster
from django.utils import timezone
from datetime import timedelta
from django.db import connections
# Create your views here.


def home(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data['employee_id']
            password = form.cleaned_data['password']
            
            # Query to match employee_id and password
            with connections['second_db'].cursor() as cursor:
                cursor.execute("""
                    SELECT SI.empId, SI.password, EM.first_name, EM.surname
                    FROM signUp AS SI
                    LEFT JOIN EmployeeMaster AS EM ON SI.empId = EM.employee_id
                    LEFT JOIN [HR].[dbo].[department] AS DP ON EM.DeptID = DP.department_id
                    WHERE SI.empId = %s 
                    AND SI.password = %s
                    AND DP.department_id = 29;
                """, [employee_id, password])

                result = cursor.fetchone()
                
                # If result is found
                if result:
                    empId = result[0]
                    first_name = result[2]
                    surname = result[3]
                    full_name = first_name +''+ surname
                    print("fullname", full_name)
                    candidate, created = HR_TABLE.objects.get_or_create(
                        name=full_name,
                        employee_id=empId
                    )
                    request.session['hr_id'] = candidate.id
                    
                    
                    return redirect('HR_dashboard')
                   
            # Render home with error message
            return render(request, 'home.html', {'form': form})

    else:
        form = CandidateForm()
    return render(request, 'home.html', {'form': form})



# # Get regions based on division ID
# def get_region(request, division_id):
#     try:
#         print(f"Getting regions for division_id: {division_id}")
#         regions = RegionMaster.objects.using('second_db').filter(divisionalid=division_id)
#          # If no regions are found
#         if not regions:
#             return JsonResponse({"error": "No regions found for this division."}, status=404)
#         regions_data = [{"region_id": region.regionid, "region_name": region.regionname} for region in regions]
#         return JsonResponse({"regions": regions_data})
#     except Exception as e:
#         # Log the error
#         print(f"Error in get_region: {str(e)}")
#         return JsonResponse({"error": "An error occurred while fetching regions."}, status=500)

# # Get units based on region ID
# def get_units(request, region_id):
#     try:
#         print("region_id ID", region_id)
        
#         units = UnitMaster.objects.using('second_db').filter(regionid=region_id)
#         units_data = [{"unit_id": unit.unitid, "unit_name": unit.unitname} for unit in units]
#         return JsonResponse({"units": units_data})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)



def get_regions(request):
    divisional_id = request.GET.get('divisionalid')
    regions = list(RegionMaster.objects.using('second_db').filter(divisionalid=divisional_id).values('regionid', 'regionname'))
    print('regions-----------',regions)
    return JsonResponse({'regions': regions})

def get_units(request):
    region_id = request.GET.get('regionid')
    units = list(UnitMaster.objects.using('second_db').filter(regionid=region_id).values('unitid', 'unitname'))
    print('units-----------',units)
    return JsonResponse({'units': units})

def get_emp(request):
    unit_id = request.GET.get('unitid')
    print('unitiddddddddddddddddddddd',unit_id)  # Debugging

    employees = list(EmployeeMaster.objects.using('second_db').filter(UnitID=unit_id).values('employee_id', 'first_name', 'DesigID', 'DeptID'))
    print('employees-----------',employees)
    return JsonResponse({'employees': employees})


# def get_emp(request):
#     unit_id = request.GET.get('unitid')
    
#     if not unit_id:
#         return JsonResponse({"error": "Unit ID is required"}, status=400)

#     # EmployeeMaster se employees filter karna
#     employees = EmployeeMaster.objects.using('second_db').filter(UnitID=unit_id).values("employee_id")

#     # Sirf unhi EmpID ko filter karega jo EmployeeMaster me hain
#     emp_ids = [emp["employee_id"] for emp in employees]
    
#     # SonataUsersKYCData se relevant employees ka data fetch karna
#     kyc_data = SonataUsersKYCData.objects.filter(EmpID__in=emp_ids).values(
#         "EmpID", "MobileNo", "AdhaarNo", "PAN_Number", "DOB", "DOJ"
#     )

#     return JsonResponse({"employees": list(kyc_data)})

# Get employees based on division, region, or unit
from django.db import connection
from django.http import JsonResponse

def get_employees(request):
    region_id = request.GET.get('region_id', None)
    unit_id = request.GET.get('unit_id', None)
    division_id = request.GET.get('division_id', None)

    try:
        # Building the WHERE conditions dynamically based on provided filters
        filters = []
        if region_id:
            filters.append(f"r.regionid = {region_id}")
        if unit_id:
            filters.append(f"b.unitid = {unit_id}")
        if division_id:
            filters.append(f"d.divisionalid = {division_id}")

        # Add the static filter for DOR
        filters.append("e.DOR = '1900-01-01 00:00:00.000'")
        # Construct the WHERE clause
        where_clause = " AND ".join(filters) if filters else "1=1"  # default to "1=1" if no filters

        # Your SQL query with the dynamic WHERE clause
        query = f"""
            SELECT 
                e.employee_id,
                e.first_name,
                e.surname,
                e.DOR,
                e.DOJ,
                d.Divisionname AS division_name,
                d.divisionalid AS division_id,
                r.regionname AS region_name,
                r.regionid AS region_id,
                b.unitname AS unit_name,
                b.unitid AS unit_id
            FROM 
                EmployeeMaster e
            LEFT JOIN 
                unitmaster b ON e.UnitID = b.unitid
            LEFT JOIN 
                regionmaster r ON b.regionid = r.regionid
            LEFT JOIN 
                Division d ON r.divisionalid = d.divisionalid
            WHERE 
                
                {where_clause} 
        """

        # Execute the query and fetch the data
        with connections['second_db'].cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        # Prepare data for the response
        employees_data = []
        for row in rows:
            employees_data.append({
                "employee_id": row[0],
                "first_name": row[1],
                "surname": row[2],
                "division_name": row[3],
                "division_id": row[4],
                "region_name": row[5],
                "region_id": row[6],
                "unit_name": row[7],
                "unit_id": row[8],
                "DOJ": row[9],
                "EmpDOB": row[10]
                
            })

        # Return the data as a JSON response
        return JsonResponse({"employees": employees_data})

    except Exception as e:
        print(f"Error in get_employees: {str(e)}")
        return JsonResponse({"error": "An error occurred while fetching employees."}, status=500)


def HR_dashboard(request):
    
    # if 'hr_id' not in request.session:
    #     return redirect('home')

    #  # Retrieve candidate_id from the session
    # hr_id = request.session.get('hr_id')
    
    divisions = Division.objects.using('second_db').all()

    # unit_ids = request.session.get('unit_ids', [])
    # print('unitidssssssssss----------',unit_ids)
    emp = SonataUsersKYCData.objects.all()
    # return render(request,'kyc_verification.html')
    return render(request,'KYC.html', {'divisions': divisions,'emp':emp})