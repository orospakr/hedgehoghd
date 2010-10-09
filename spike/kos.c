/* This file is in the public domain. */

#include <stdio.h>
#include <stdlib.h>

/*
 * Kosinski decompresser, for compression such as is used for Sonic and
 *  Sonic 2 level data.
 *
 * This is based on http://segaretro.org/Kosinski_compression, but
 *  beware that (at least as of this writing) that page contains
 *  errors.  In particular, the examples which look like test vectors
 *  are broken.  Description field reading is greedy - a new
 *  description field is read as soon as the last bit of the previous
 *  one is consumed, rather than waiting until a bit is needed from the
 *  next one - which means that, to pick the first example,
 *
 *	FF FF 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
 *
 *  will not work - it will try to read a new description field after
 *  reading the 0E byte, with the sixteenth data byte being read after
 *  that new description field.
 *
 * A careful study of the 68k assembly code makes this clear, and this
 *  decompresser, which was written to do greedy description field
 *  reading, does seem to work.
 *
 * The webpage uses the term "run-length encoding" incorrectly.  It
 *  uses it to refer to any backreference in the output stream; this
 *  can be used to do run-length encoding by specifying a copy-from
 *  offset of -1, but it can also do a lot more, and definitely is not
 *  what RLE is normally used (and understood) to mean.  This program
 *  avoids this misnomer.
 *
 * Produces extremely verbose output as it walks the input data; at
 *  end-of-data, dumps the resulting output block.
 */

int main(void);
int main(void)
{
 /*
  * desc is the current description field; descbits is the number of
  *  valid bits in it.  Rather than bit-reverse the description field
  *  bytes the way the segaretro.org page does, we just read them out
  *  low bit first, the way the 68k code does.
  */
 unsigned short int desc;
 int descbits;
 /*
  * Output block.  Actual levels do not go beyond 4096.  We really
  *  should check that this buffer doesn't overflow; see outb().
  */
 unsigned char obuf[8192];
 /*
  * Pointer into obuf where output is written.
  */
 unsigned char *obp;
 /*
  * During decompression, n is a count of bytes to copy and o is the
  *  offset to copy them from (o will always be negative).  When
  *  dumping the output, o is the amount of output data and n is an
  *  index counting from 0 to o-1.
  */
 int n;
 int o;
 /*
  * Source pointer when doing backreference copies.
  */
 unsigned char *cp;

 /*
  * Get the next input byte.  Errors if it reaches EOF, since that
  *  means we have mangled data - truncated, or corrupted enough that
  *  we missed the end-of-data marker.
  */
 unsigned int gc(void)
  { int c;
    c = getchar();
    if (c == EOF)
     { printf("unexpected EOF\n");
       exit(1);
     }
    printf("gc: %02x\n",c);
    return(c);
  }

 /*
  * Read the next description field.  Note that the first two
  *  assignments cannot be combined because there needs to be a
  *  sequence point to ensure the calls to gc() are made in the correct
  *  order.
  */
 void getdesc(void)
  { desc = gc();
    desc |= gc() * 256;
    descbits = 16;
    printf("getdesc: desc = %04x\n",desc);
  }

 /*
  * Get the next description field bit.  This is responsible for
  *  greedily reading the next description field when it runs out of
  *  bits in the current one.
  */
 int descbit(void)
  { int bit;
    bit = desc & 1;
    desc >>= 1;
    descbits --;
    if (descbits == 0) getdesc();
    printf("descbit: %d\n",bit);
    return(bit);
  }

 /*
  * Output a byte.  We call this rather than just storing through obp
  *  directly so as to log output bytes.
  */
 void outb(unsigned char c)
  { printf("out: %02x\n",c);
    *obp++ = c;
  }

 /*
  * Set up: initialize the output pointer and read the first
  *  description field.
  */
 obp = &obuf[0];
 getdesc();
 /*
  * Decompression loop.  We break from this loop upon finding an
  *  end-of-data marker (or exit on error).
  */
 while (1)
  { if (descbit())
     { /*
	* Uncompressed byte.  Just log, fetch, and save.
	*/
       printf("uncompressed\n");
       outb(gc());
     }
    else
     { if (descbit())
	{ /*
	   * Long copy, or special.  This is what the webpage calls
	   *  "separate run-length encoding".
	   */
	  printf("long copy\n");
	  o = gc() - 8192;
	  n = gc();
	  o += (n & 0xf8) << 5;
	  if (n & 7)
	   { /* Two-byte version. */
	     n = (n & 7) + 2;
	   }
	  else
	   { /* Three-byte version, including specials. */
	     n = gc();
	     if (n == 0) break;
	     if (n == 1)
	      { getdesc();
		continue;
	      }
	     n ++;
	   }
	}
       else
	{ /*
	   * Short copy.  This is what the webpage calls "inline
	   *  run-length encoding".
	   */
	  printf("short copy\n");
	  n = descbit() * 2;
	  n += descbit() + 2;
	  o = gc() - 256;
	}
       /*
	* Common code for short and lonjg copies.  At this point,
	*  everything has been read except for the actual data, and n
	*  and o have been set up to describe the copy.
	*/
       printf("copy %d from %d\n",n,o);
       if (-o > obp-&obuf[0])
	{ printf("offset %d > output length %d\n",o,(int)(obp-&obuf[0]));
	  exit(1);
	}
       cp = obp + o;
       for (;n>0;n--) outb(*cp++);
     }
  }
 /*
  * The above code found an end-of-data marker and broke from the
  *  decompression loop.  Report it and dump the output data.
  */
 printf("Marker seen\n");
 o = obp - &obuf[0];
 for (n=0;n<o;n++)
  { switch (n & 15)
     { case 0:
	  printf("%03x: ",n);
	  break;
       case 8:
	  printf(" ");
	  break;
     }
    printf(" %02x",obuf[n]);
    switch (n & 15)
     { case 15:
	  printf("\n");
	  break;
     }
  }
 switch (o & 15)
  { case 0:
       break;
    default:
       printf("\n");
       break;
  }
 return(0);
}
