package com.conference.attendees.model;

import jakarta.persistence.*;
import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.Objects;

/**
 * JPA Entity representing an attendee in the database.
 * This follows the traditional anemic domain model approach.
 */
@Entity
@Table(name = "attendees")
@NamedQueries({
    @NamedQuery(name = "AttendeeEntity.findAll",
                query = "SELECT a FROM AttendeeEntity a"),
    @NamedQuery(name = "AttendeeEntity.findByEmail",
                query = "SELECT a FROM AttendeeEntity a WHERE a.email = :email")
})
public class AttendeeEntity implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "email", unique = true, nullable = false)
    private String email;

    @Column(name = "first_name", nullable = false)
    private String firstName;

    @Column(name = "last_name", nullable = false)
    private String lastName;

    @Embedded
    private Address address;

    @Column(name = "registration_date")
    private LocalDateTime registrationDate;

    @Column(name = "status")
    @Enumerated(EnumType.STRING)
    private AttendeeStatus status;

    public AttendeeEntity() {
        this.registrationDate = LocalDateTime.now();
        this.status = AttendeeStatus.REGISTERED;
    }

    public AttendeeEntity(String email, String firstName, String lastName, Address address) {
        this();
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
        this.address = address;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public Address getAddress() {
        return address;
    }

    public void setAddress(Address address) {
        this.address = address;
    }

    public LocalDateTime getRegistrationDate() {
        return registrationDate;
    }

    public void setRegistrationDate(LocalDateTime registrationDate) {
        this.registrationDate = registrationDate;
    }

    public AttendeeStatus getStatus() {
        return status;
    }

    public void setStatus(AttendeeStatus status) {
        this.status = status;
    }

    // Business method - will be moved to aggregate later
    public String getFullName() {
        return firstName + " " + lastName;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        AttendeeEntity that = (AttendeeEntity) o;
        return Objects.equals(email, that.email);
    }

    @Override
    public int hashCode() {
        return Objects.hash(email);
    }

    @Override
    public String toString() {
        return "AttendeeEntity{" +
                "id=" + id +
                ", email='" + email + '\'' +
                ", firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", address=" + address +
                ", registrationDate=" + registrationDate +
                ", status=" + status +
                '}';
    }

    public enum AttendeeStatus {
        REGISTERED,
        CONFIRMED,
        CANCELLED
    }
}