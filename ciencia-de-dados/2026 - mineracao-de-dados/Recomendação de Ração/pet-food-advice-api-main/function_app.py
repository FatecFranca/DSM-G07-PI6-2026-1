import json
import azure.functions as func
import logging
from dog_food import get_food_recommendations, check_if_breed_exists, rank_products

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


def validate_format_breed(breed):
    if not isinstance(breed, str):
        return func.HttpResponse("Breed must be a string.", status_code=400)
    else:
        if not check_if_breed_exists(breed):
            breed = None
    return breed


def validate_format_animalWeight(animalWeight):
    if not (isinstance(animalWeight, int) or isinstance(animalWeight, float)):
        return func.HttpResponse("Animal weight must be a number.", status_code=400)
    else:
        if animalWeight >= 70:
            animalWeight = "Giant"
        elif animalWeight >= 50:
            animalWeight = "Large"
        elif animalWeight >= 25:
            animalWeight = "Medium"
        elif animalWeight >= 12:
            animalWeight = "Small"
        else:
            animalWeight = "X-Small"
    return animalWeight


def validate_format_age(age):
    if not (isinstance(age, int) or isinstance(age, float)):
        return func.HttpResponse("Age must be a number.", status_code=400)
    else:
        if age >= 7:
            age = "Senior"
        elif age >= 2:
            age = "Adult"
        else:
            age = "Puppy"
    return age


def validate_format_conditions(conditions):
    condition_mapping = {
        "Food Allergy": "Allergies or Food Sensitivities",
        "Sensitive Stomach & Skin": "Allergies or Food Sensitivities",
        "Overweight": "Overweight",
        "Skin and Coat Health": "Skin/Coat problems",
        "Digestive Care": "Digestive issues",
        "Joint Care": "Mobility concerns",
        "Dental Care": "Dental issues",
        "Urinary Care": "Urinary problems",
    }

    recognized_conditions = ", ".join(
        set(condition_mapping.keys()).union(set(condition_mapping.values()))
    )

    if not (
        isinstance(conditions, list)
        and all(isinstance(cond, str) for cond in conditions)
    ):
        return func.HttpResponse(
            "Conditions must be an array of strings.", status_code=400
        )

    for condition in conditions:
        if (
            condition not in condition_mapping
            and condition not in condition_mapping.values()
        ):
            error_message = (
                f"The condition '{condition}' is not recognized. "
                f"Recognized conditions are: {recognized_conditions}."
            )
            return func.HttpResponse(error_message, status_code=400)

    return conditions


