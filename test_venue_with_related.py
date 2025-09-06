#!/usr/bin/env python3
"""
Test script to verify CreateVenueSerializer creates scavenger hunts and venue messages
"""
import os
import sys
import django
from django.conf import settings

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from services.models import City, PlaceType, Venue, ScavengerHunt, List_Message
from services.serializers import CreateVenueSerializer

def test_create_venue_with_related_objects():
    """Test CreateVenueSerializer to ensure it creates scavenger hunts and messages"""
    
    print("🧪 Testing CreateVenueSerializer with related objects...")
    print("=" * 60)
    
    # Create test data
    city = City.objects.get_or_create(
        name="Test City for Related Objects",
        defaults={'description': "A test city for serializer testing"}
    )[0]
    
    place_type = PlaceType.objects.get_or_create(
        name="Test Restaurant",
        defaults={'description': "Food establishment for testing"}
    )[0]
    
    # Count initial objects
    initial_venue_count = Venue.objects.count()
    initial_scavenger_hunt_count = ScavengerHunt.objects.count()
    initial_message_count = List_Message.objects.count()
    
    print(f"📊 Initial counts:")
    print(f"   Venues: {initial_venue_count}")
    print(f"   Scavenger Hunts: {initial_scavenger_hunt_count}")
    print(f"   Messages: {initial_message_count}")
    print()
    
    # Test venue data with scavenger hunts and messages
    venue_data = {
        'city': city.id,
        'type_of_place': place_type.id,
        'venue_name': 'Test Restaurant with Related Objects',
        'description': 'A test restaurant with scavenger hunts and messages',
        'latitude': 40.7128,
        'longitude': -74.0060,
        'scavenger_hunts': [
            {'title': 'Find the hidden treasure'},
            {'title': 'Take a photo with the chef'},
            {'title': 'Order the special dish'}
        ],
        'venue_message': [
            {'message': 'Welcome to our restaurant!'},
            {'message': 'Don\'t forget to try our signature dish!'}
        ]
    }
    
    # Create and validate serializer
    print("🏗️  Creating venue with scavenger hunts and messages...")
    serializer = CreateVenueSerializer(data=venue_data)
    
    if not serializer.is_valid():
        print(f"❌ Serializer validation failed: {serializer.errors}")
        return False
    
    # Save the venue
    venue = serializer.save()
    print(f"✅ Venue created successfully: {venue.venue_name}")
    
    # Count objects after creation
    final_venue_count = Venue.objects.count()
    final_scavenger_hunt_count = ScavengerHunt.objects.count()
    final_message_count = List_Message.objects.count()
    
    print(f"\n📊 Final counts:")
    print(f"   Venues: {final_venue_count} (Expected: {initial_venue_count + 1})")
    print(f"   Scavenger Hunts: {final_scavenger_hunt_count} (Expected: {initial_scavenger_hunt_count + 3})")
    print(f"   Messages: {final_message_count} (Expected: {initial_message_count + 2})")
    
    # Verify venue details
    print(f"\n🏢 Venue Details:")
    print(f"   ID: {venue.id}")
    print(f"   Name: {venue.venue_name}")
    print(f"   City: {venue.city.name}")
    print(f"   Type: {venue.type_of_place.name}")
    print(f"   Latitude: {venue.latitude}")
    print(f"   Longitude: {venue.longitude}")
    print(f"   Description: {venue.description}")
    
    # Check related objects for this venue
    venue_scavenger_hunts = venue.scavenger_hunts.all()
    venue_messages = venue.messages.all()
    
    print(f"\n🔗 Related Objects for this venue:")
    print(f"   Scavenger Hunts: {venue_scavenger_hunts.count()}")
    for hunt in venue_scavenger_hunts:
        print(f"      - {hunt.title}")
    
    print(f"   Messages: {venue_messages.count()}")
    for message in venue_messages:
        print(f"      - {message.message}")
    
    # Test serializer representation
    print(f"\n📄 Serializer Representation:")
    representation = serializer.to_representation(venue)
    print(f"   Venue Name: {representation['venue_name']}")
    print(f"   City: {representation['city']}")
    print(f"   Type: {representation['type_of_place']}")
    print(f"   Scavenger Hunts ({len(representation['scavenger_hunts'])}):")
    for hunt in representation['scavenger_hunts']:
        print(f"      - {hunt['title']}")
    print(f"   Messages ({len(representation['venue_message'])}):")
    for msg in representation['venue_message']:
        print(f"      - {msg['message']}")
    
    # Verify test results
    print(f"\n🎯 Test Results:")
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Venue was created
    if final_venue_count == initial_venue_count + 1:
        print("   ✅ Venue creation: PASSED")
        tests_passed += 1
    else:
        print("   ❌ Venue creation: FAILED")
    
    # Test 2: Scavenger hunts created
    expected_hunts = initial_scavenger_hunt_count + 3
    if final_scavenger_hunt_count == expected_hunts:
        print("   ✅ Scavenger hunts created: PASSED")
        tests_passed += 1
    else:
        print(f"   ❌ Scavenger hunts created: FAILED (Expected: {expected_hunts}, Got: {final_scavenger_hunt_count})")
    
    # Test 3: Messages created
    expected_messages = initial_message_count + 2
    if final_message_count == expected_messages:
        print("   ✅ Messages created: PASSED")
        tests_passed += 1
    else:
        print(f"   ❌ Messages created: FAILED (Expected: {expected_messages}, Got: {final_message_count})")
    
    # Test 4: Venue has correct number of scavenger hunts
    if venue_scavenger_hunts.count() == 3:
        print("   ✅ Venue has correct scavenger hunts: PASSED")
        tests_passed += 1
    else:
        print(f"   ❌ Venue has correct scavenger hunts: FAILED (Expected: 3, Got: {venue_scavenger_hunts.count()})")
    
    # Test 5: Venue has correct number of messages
    if venue_messages.count() == 2:
        print("   ✅ Venue has correct messages: PASSED")
        tests_passed += 1
    else:
        print(f"   ❌ Venue has correct messages: FAILED (Expected: 2, Got: {venue_messages.count()})")
    
    # Test 6: Representation includes all data
    if (len(representation['scavenger_hunts']) == 3 and 
        len(representation['venue_message']) == 2):
        print("   ✅ Serializer representation complete: PASSED")
        tests_passed += 1
    else:
        print("   ❌ Serializer representation complete: FAILED")
    
    print(f"\n🏆 Summary: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests PASSED! CreateVenueSerializer creates related objects correctly.")
        return True
    else:
        print("⚠️  Some tests FAILED! Please check the implementation.")
        return False

def test_create_venue_without_related_objects():
    """Test CreateVenueSerializer works without scavenger hunts and messages"""
    print("\n🔍 Testing venue creation without related objects...")
    print("=" * 50)
    
    # Create test data
    city = City.objects.get_or_create(
        name="Simple Test City",
        defaults={'description': "A simple test city"}
    )[0]
    
    place_type = PlaceType.objects.get_or_create(
        name="Simple Cafe",
        defaults={'description': "Simple cafe type"}
    )[0]
    
    # Test venue data without scavenger hunts and messages
    venue_data = {
        'city': city.id,
        'type_of_place': place_type.id,
        'venue_name': 'Simple Test Cafe Without Related Objects',
        'description': 'A simple cafe without related objects',
        'latitude': 41.8781,
        'longitude': -87.6298
        # No scavenger_hunts or venue_message fields
    }
    
    # Create and validate serializer
    serializer = CreateVenueSerializer(data=venue_data)
    
    if not serializer.is_valid():
        print(f"❌ Serializer validation failed: {serializer.errors}")
        return False
    
    # Save the venue
    venue = serializer.save()
    print(f"✅ Simple venue created: {venue.venue_name}")
    
    # Check that no related objects were created
    venue_scavenger_hunts = venue.scavenger_hunts.count()
    venue_messages = venue.messages.count()
    
    print(f"   Scavenger Hunts: {venue_scavenger_hunts} (Expected: 0)")
    print(f"   Messages: {venue_messages} (Expected: 0)")
    
    if venue_scavenger_hunts == 0 and venue_messages == 0:
        print("✅ Simple venue creation works correctly")
        return True
    else:
        print("❌ Simple venue creation failed")
        return False

if __name__ == "__main__":
    try:
        print("🚀 Starting CreateVenueSerializer Tests with Related Objects")
        print("=" * 70)
        
        # Run tests
        test1_result = test_create_venue_with_related_objects()
        test2_result = test_create_venue_without_related_objects()
        
        print("\n" + "=" * 70)
        if test1_result and test2_result:
            print("🎉 ALL TESTS PASSED!")
            print("✨ CreateVenueSerializer creates venues with scavenger hunts and messages correctly.")
            print("📝 It also works when no related objects are provided.")
        else:
            print("⚠️  SOME TESTS FAILED!")
            print("🔧 Please review the serializer implementation.")
            
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
