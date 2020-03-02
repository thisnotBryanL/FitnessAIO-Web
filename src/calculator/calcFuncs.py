def convertToCenti(height):
    return round(height * 2.54,1)

def convertToKilos(weight):
    return round(weight/2.205,1)

# Height = inches
def calorieCalc(weight,choice,gender,height,age):
    if choice == 'seditary':
        bodyFat = .20
        activityMult = 1.3
    elif choice == 'average':
        bodyFat = .15
        activityMult = 1.6
    else:
        bodyFat = .12
        activityMult = 1.9

    weight = convertToKilos(weight)
    height = convertToCenti(height)

    print("Weight (KG) = ", weight)
    print ("Height (Centi) = " , height)

    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    calories = round(bmr * activityMult,1)
    return calories


calories = calorieCalc(150, 'average', 'male', 67, 25)
print ('My calories = ', calories)
print()

def macroCalc(weight,choice,calories):
    macros = dict()

    if choice == 'seditary':
        bodyFat = .20
        proteinFactor = 1.3
    elif choice == 'average':
        bodyFat = .15
        proteinFactor = 1.4
    else:
        bodyFat = .12
        proteinFactor = 1.5
    
    lean_mass = 1 - bodyFat
    lean_body_mass = weight * lean_mass

    protein_macros = round(lean_body_mass * proteinFactor)
    
    fat_macros = round((calories * 0.25)/9)

    cur_calories = (protein_macros * 4) + (fat_macros * 9)
    
    carb_calories = calories - cur_calories
    carb_macros = round(carb_calories/4)

    macros['protein'] = protein_macros
    macros['fat'] = fat_macros
    macros['carbs'] = carb_macros

    return macros

my_macros = macroCalc(150,'male',calories)
print(my_macros['fat'])