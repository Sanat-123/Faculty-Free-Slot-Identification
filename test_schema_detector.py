from import_engine.schema_detector import SchemaDetector


print("=" * 80)
print("UNISCHED AI - UNIVERSAL SCHEMA DETECTOR TEST")
print("=" * 80)


# ======================================================
# Test 1 - Your actual Excel column names
# ======================================================

columns = [
    "class",
    "teacher",
    "group",
    "subject",
    "length",
    "lessons/week",
    "available classrooms",
    "cycle",
    "classrooms",
]


print("\n1. INPUT COLUMNS")
print("-" * 80)

for column in columns:
    print(column)


# ======================================================
# Test 2 - Detect schema
# ======================================================

result = SchemaDetector.detect(
    columns
)


print("\n2. DETECTED SCHEMA")
print("-" * 80)

for column, information in result["detected"].items():

    print(
        f"{column} -> "
        f"{information['field']} "
        f"({information['confidence']}%)"
    )


# ======================================================
# Test 3 - Unknown columns
# ======================================================

print("\n3. UNKNOWN COLUMNS")
print("-" * 80)

if result["unknown"]:

    for column in result["unknown"]:
        print(column)

else:

    print("None")


# ======================================================
# Test 4 - Universal mapping
# ======================================================

print("\n4. UNIVERSAL MAPPING")
print("-" * 80)

mapping = (
    SchemaDetector.get_universal_mapping(
        columns
    )
)

for original, universal in mapping.items():

    print(
        f"{original} -> {universal}"
    )


# ======================================================
# Test 5 - Dataset capabilities
# ======================================================

print("\n5. DATASET CAPABILITIES")
print("-" * 80)

capabilities = (
    SchemaDetector.detect_capabilities(
        columns
    )
)

for capability, supported in (
    capabilities.items()
):

    print(
        f"{capability}: {supported}"
    )


# ======================================================
# Test 6 - Required fields
# ======================================================

print("\n6. AVAILABLE / MISSING FIELDS")
print("-" * 80)

required = (
    SchemaDetector.check_required_fields(
        columns
    )
)

print(
    "Available:"
)

for field in required["available"]:
    print(
        f"  ✓ {field}"
    )

print(
    "\nMissing:"
)

for field in required["missing"]:
    print(
        f"  - {field}"
    )


print("\n" + "=" * 80)
print("SCHEMA DETECTOR TEST COMPLETED")
print("=" * 80)