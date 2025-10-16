# Scavenger Hunt Image Support - FormData Example

## Updated Serializers

Both `CreateVenueSerializer` and `UpdateVenueSerializer` now support image uploads for scavenger hunts.

## FormData Format

When sending data from the frontend, use this FormData structure:

### Basic Venue Data

```
venue_name: "Example Venue"
city: 1
type_of_place: 2
description: "A great venue"
latitude: 40.7128
longitude: -74.0060
image: [FILE] (venue image file)
```

### Scavenger Hunts with Images

```
scavenger_hunts[0][title]: "Find the red door"
scavenger_hunts[0][image]: [FILE] (scavenger hunt image file)

scavenger_hunts[1][title]: "Take a photo with the statue"
scavenger_hunts[1][image]: [FILE] (another scavenger hunt image file)

scavenger_hunts[2][title]: "Text only hunt"
(no image for this one)
```

### Venue Messages

```
venue_message[0][message]: "Welcome to our venue!"
venue_message[1][message]: "Don't forget to check in!"
```

## JavaScript Example

```javascript
const formData = new FormData();

// Basic venue data
formData.append("venue_name", "Example Venue");
formData.append("city", "1");
formData.append("type_of_place", "2");
formData.append("description", "A great venue");
formData.append("latitude", "40.7128");
formData.append("longitude", "-74.0060");
formData.append("image", venueImageFile); // File object

// Scavenger hunts
formData.append("scavenger_hunts[0][title]", "Find the red door");
formData.append("scavenger_hunts[0][image]", scavengerImage1); // File object

formData.append("scavenger_hunts[1][title]", "Take a photo with the statue");
formData.append("scavenger_hunts[1][image]", scavengerImage2); // File object

// Venue messages
formData.append("venue_message[0][message]", "Welcome to our venue!");
formData.append("venue_message[1][message]", "Don't forget to check in!");

// Send the request
fetch("/api/venues/create/", {
  method: "POST",
  body: formData,
  headers: {
    Authorization: "Bearer your-token-here",
  },
});
```

## Model Changes

The ScavengerHunt model already supports images:

```python
class ScavengerHunt(models.Model):
    venue = models.ForeignKey('Venue', related_name='scavenger_hunts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="scavenger_hunts/", null=True, blank=True)  # ✅ Already exists
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
```

## Response Format

The response will include scavenger hunts with their images:

```json
{
  "id": 1,
  "city": "New York",
  "type_of_place": "Restaurant",
  "venue_name": "Example Venue",
  "image": "/media/venue_images/example.jpg",
  "description": "A great venue",
  "latitude": 40.7128,
  "longitude": -74.006,
  "scavenger_hunts": [
    {
      "id": 1,
      "title": "Find the red door",
      "image": "/media/scavenger_hunts/red_door.jpg",
      "check": {
        "checked": false,
        "uploaded_image": null
      }
    },
    {
      "id": 2,
      "title": "Take a photo with the statue",
      "image": "/media/scavenger_hunts/statue.jpg",
      "check": {
        "checked": false,
        "uploaded_image": null
      }
    }
  ],
  "venue_message": [
    {
      "id": 1,
      "message": "Welcome to our venue!"
    }
  ]
}
```
