package com.conference.attendees.model;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import java.io.Serializable;
import java.util.Objects;

/**
 * Traditional POJO representing an address.
 * This will be refactored to a DDD Value Object later.
 */
@Embeddable
public class Address implements Serializable {

    @Column(name = "street_address")
    private String streetAddress;

    @Column(name = "bus")
    private String bus;

    @Column(name = "postal_code")
    private String postalCode;

    @Column(name = "town_or_municipality")
    private String townOrMunicipality;

    public Address() {
        // Default constructor for JPA and serialization
    }

    public Address(String streetAddress, String bus, String postalCode, String townOrMunicipality) {
        this.streetAddress = streetAddress;
        this.bus = bus;
        this.postalCode = postalCode;
        this.townOrMunicipality = townOrMunicipality;
    }

    // Basic validation in setters (traditional approach)
    public String getStreetAddress() {
        return streetAddress;
    }

    public void setStreetAddress(String streetAddress) {
        if (streetAddress == null || streetAddress.trim().isEmpty()) {
            throw new IllegalArgumentException("Street address cannot be null or empty");
        }
        this.streetAddress = streetAddress;
    }

    public String getBus() {
        return bus;
    }

    public void setBus(String bus) {
        this.bus = bus;
    }

    public String getPostalCode() {
        return postalCode;
    }

    public void setPostalCode(String postalCode) {
        if (postalCode == null || postalCode.trim().isEmpty()) {
            throw new IllegalArgumentException("Postal code cannot be null or empty");
        }
        this.postalCode = postalCode;
    }

    public String getTownOrMunicipality() {
        return townOrMunicipality;
    }

    public void setTownOrMunicipality(String townOrMunicipality) {
        if (townOrMunicipality == null || townOrMunicipality.trim().isEmpty()) {
            throw new IllegalArgumentException("Town or municipality cannot be null or empty");
        }
        this.townOrMunicipality = townOrMunicipality;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Address address = (Address) o;
        return Objects.equals(streetAddress, address.streetAddress) &&
                Objects.equals(bus, address.bus) &&
                Objects.equals(postalCode, address.postalCode) &&
                Objects.equals(townOrMunicipality, address.townOrMunicipality);
    }

    @Override
    public int hashCode() {
        return Objects.hash(streetAddress, bus, postalCode, townOrMunicipality);
    }

    @Override
    public String toString() {
        return "Address{" +
                "streetAddress='" + streetAddress + '\'' +
                ", bus='" + bus + '\'' +
                ", postalCode='" + postalCode + '\'' +
                ", townOrMunicipality='" + townOrMunicipality + '\'' +
                '}';
    }
}