# CAPWATCH Download

This script will download a CAPWATCH database from eServices.

usage: get_capwatch.py [-h] -u USERNAME -p PASSWORD -o ORGANIZATION
                       [-f FILENAME]

Organization is a numeric value that can be found by looking at the source
of the CAPWATCH download page in eServices. For example, you might see:

```html
<option selected="selected" value="490">GLR-MI-063</option>
```

In this case, the organization is 490.
