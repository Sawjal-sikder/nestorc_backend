#!/usr/bin/env python3
"""
Test script to verify CreateVenueSerializer handles FormData format
"""
import os
import sys
import django
from django.http import QueryDict

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from services.models import City, PlaceType, Venue, ScavengerHunt, List_Message
from services.serializers import CreateVenueSerializer

def test_formdata_parsing():
    """Test CreateVenueSerializer with FormData-like input"""
    
    print("🧪 Testing CreateVenueSerializer with FormData format...")
    print("=" * 60)
    
    # Get or create test data
    city = City.objects.get_or_create(
        name="FormData Test City",
        defaults={'description': "Test city for FormData"}
    )[0]
    
    place_type = PlaceType.objects.get_or_create(
        name="FormData Test Type",
        defaults={'description': "Test place type for FormData"}
    )[0]
    
    print(f"🏙️  Using City: {city.name} (ID: {city.id})")
    print(f"🏪 Using Place Type: {place_type.name} (ID: {place_type.id})")
    print()
    
    # Simulate FormData format (similar to what frontend sends)
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    query_dict = QueryDict(mutable=True)
    query_dict.update({
        'venue_name': f'FormData Test Venue {timestamp}',
        'description': 'A venue created from FormData',
        'latitude': '32.788384327862666',
        'longitude': '-96.84265883061337',
        'city': str(city.id),
        'type_of_place': str(place_type.id),
        'scavenger_hunts[0][title]': 'FormData Scavenger Hunt 1',
        'scavenger_hunts[1][title]': 'FormData Scavenger Hunt 2',
        'venue_message[0][message]': 'FormData Message 1',
        'venue_message[1][message]': 'FormData Message 2',
    })
    
    print("📝 Input FormData:")
    for key, value in query_dict.items():
        print(f"   {key}: {value}")
    print()
    
    # Count initial objects
    initial_venue_count = Venue.objects.count()
    initial_scavenger_hunt_count = ScavengerHunt.objects.count()
    initial_message_count = List_Message.objects.count()
    
    print(f"📊 Initial counts:")
    print(f"   Venues: {initial_venue_count}")
    print(f"   Scavenger Hunts: {initial_scavenger_hunt_count}")
    print(f"   Messages: {initial_message_count}")
    print()
    
    # Create serializer and validate
    serializer = CreateVenueSerializer(data=query_dict)
    
    if serializer.is_valid():
        venue = serializer.save()
        print(f"✅ Venue created successfully!")
        print(f"   ID: {venue.id}")
        print(f"   Name: {venue.venue_name}")
        print()
        
        # Check created objects
        hunts = venue.scavenger_hunts.all()
        messages = venue.messages.all()
        
        print(f"🎲 Created Scavenger Hunts ({hunts.count()}):")
        for hunt in hunts:
            print(f"   - {hunt.title}")
        print()
        
        print(f"💬 Created Messages ({messages.count()}):")
        for message in messages:
            print(f"   - {message.message}")
        print()
        
        # Verify counts
        final_venue_count = Venue.objects.count()
        final_scavenger_hunt_count = ScavengerHunt.objects.count()
        final_message_count = List_Message.objects.count()
        
        print(f"📊 Final counts:")
        print(f"   Venues: {final_venue_count} (Expected: {initial_venue_count + 1})")
        print(f"   Scavenger Hunts: {final_scavenger_hunt_count} (Expected: {initial_scavenger_hunt_count + 2})")
        print(f"   Messages: {final_message_count} (Expected: {initial_message_count + 2})")
        
        # Check results
        venue_created = final_venue_count == initial_venue_count + 1
        hunts_created = final_scavenger_hunt_count == initial_scavenger_hunt_count + 2
        messages_created = final_message_count == initial_message_count + 2
        venue_hunts_correct = hunts.count() == 2
        venue_messages_correct = messages.count() == 2
        
        print("\n🎯 Test Results:")
        print(f"   ✅ Venue created: {'PASSED' if venue_created else 'FAILED'}")
        print(f"   ✅ Scavenger hunts created: {'PASSED' if hunts_created else 'FAILED'}")
        print(f"   ✅ Messages created: {'PASSED' if messages_created else 'FAILED'}")
        print(f"   ✅ Venue has correct hunts: {'PASSED' if venue_hunts_correct else 'FAILED'}")
        print(f"   ✅ Venue has correct messages: {'PASSED' if venue_messages_correct else 'FAILED'}")
        
        all_passed = all([venue_created, hunts_created, messages_created, venue_hunts_correct, venue_messages_correct])
        
        if all_passed:
            print("\n🎉 SUCCESS! FormData parsing works correctly!")
            return True
        else:
            print("\n⚠️ Some tests failed!")
            return False
    else:
        print(f"❌ Serializer validation failed: {serializer.errors}")
        return False

if __name__ == "__main__":
    try:
        print("🚀 Starting FormData Parsing Test")
        print("=" * 60)
        
        result = test_formdata_parsing()
        
        print("\n" + "=" * 60)
        if result:
            print("🎉 FORMDATA TEST PASSED!")
            print("✨ CreateVenueSerializer correctly handles FormData format!")
            print("📝 Frontend nested arrays are properly parsed and processed.")
        else:
            print("⚠️ FORMDATA TEST FAILED!")
            print("🔧 Please check the serializer implementation.")
            
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
